import requests
import stripe
import logging
from django.shortcuts import render, get_object_or_404, reverse, redirect, resolve_url
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.dispatch import receiver
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated


from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import valid_ipn_received

from .models import Payment
from users.models import User

logger = logging.getLogger(__file__)

stripe.api_key = settings.STRIPE_SECRET_KEY

# Generate an invoice
# INVOICE = "unique_invoice_00001"


@login_required
def payment(request, amount=0.0):
    print(f'>>> PAYMENTS @ payment: Amount {amount}')
    logger.info(f'>>> PAYMENTS @ payment: Amount {amount}')
    deposit_id = request.session.get('order_id')
    context = {}
    host = request.get_host()
    user = request.user

    invoice = Payment.objects.create(
        amount=amount,
        user=user
    )

    ipn_url = (
        # settings.PAYPAL_IPN_URL or
        'http://{}{}'.format(host, reverse('payments:paypal-ipn'))
    )
    # PayPal Payments
    #################
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": amount,
        "currency": settings.CURRENCY,
        "locale": 'en_US',
        "style": {
            "size": 'medium',
            "color": 'blue',
            "shape": 'pill',
            "label": 'Deposit',
            "tagline": 'true'
        },
        "item_name": "Deposit",
        "invoice": invoice.id,
        "notify_url": ipn_url,
        "return_url": f"http://{host}/payments/paypal_return/",
        "cancel_url": f"http://{host}/payments/paypal_cancel/"
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

    # Paypal: Adding the amount to the user's balance
    # user.balance = user.balance + amount
    # user.save()
    
    # print(f">>> PAYMENTS @ payment: Updated user balance with additional {amount}")
    # logger.info(f">>> PAYMENTS @ payment: Updated user balance with additional {amount}")

    context['form'] = form
    context['amount'] = amount
    context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
    return render(request, 'payments/payment.html', context)


@login_required
def stripe_payment(request, amount=0.0):
    print(f'>>> PAYMENTS @ stripe_payment: Amount {amount}')
    logger.info(f'>>> PAYMENTS @ stripe_payment: Amount {amount}')
    context = {}
    context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
    context['amount'] = amount
    return render(request, 'payments/stripe_payment.html', context)


@login_required
def charge(request):
    print(f">>> PAYMENTS @ charge (Stripe)")
    logger.info(f">>> PAYMENTS @ charge (Stripe)")

    if request.method == 'POST':
        print('Charge info:', request.POST)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        user = User.objects.get(pk=request.user.pk)
        name = user.name
        email = user.email
        amount = float(request.POST.get('amount'))
        try:
            if not user.stripe_customer_key:
                customer = stripe.Customer.create(
                    name=name,
                    email=email,
                    source=request.POST['stripeToken']
                )

                response = stripe.Charge.create(
                    customer=customer,
                    amount=int(amount * 100),
                    currency="usd",  # TODO: make dynamic according to browser language
                    description="PolyBingo funds deposit",
                )

                # Adding stripe customer key to the user
                user.stripe_customer_key = customer.id
            else:
                response = stripe.Charge.create(
                    customer=user.stripe_customer_key,
                    amount=int(amount * 100),
                    currency="usd",  # TODO: make dynamic according to browser language
                    description="PolyBingo funds deposit",
                )
        except Exception as e:
            messages.error(request, _("Something went wrong with your payment. Your account balance was not updated."))
            return HttpResponseRedirect(reverse("bingo_main:dashboard"))

    # Stripe payment: Adding the amount to the user's balance
    user.balance = user.balance + amount
    user.save()

    # TODO Send invoice to user.

    print(f">>> PAYMENTS @ charge (Stripe): Updated user balance with additional {amount}")
    logger.info(f">>> PAYMENTS @ charge (Stripe): Updated user balance with additional {amount}")

    # return redirect(reverse('payments:success', args=[amount]))
    messages.success(request, _("Thank you for the payment. You should see your updated balance shortly."))
    return HttpResponseRedirect(reverse("bingo_main:dashboard"))


def successMsg(request, args):
    amount = args
    return render(request, 'payments/success.html', {'amount': amount})


@login_required
def deposits(request):
    context = {}
    if request.method == 'POST':
        if 'deposit_amount' in request.POST:
            amount = request.POST.get('deposit_amount')
            if amount != '':
                return HttpResponseRedirect(reverse('payment', args=[amount]))
            else:
                messages.error(request, _('Please enter an amount, or pick pf the predefined amounts.'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'payments/deposits.html', context)


@csrf_exempt
def paypal_return(request):
    user = request.user
    payment = Payment.objects.filter(user=user).last()
    amount = payment.amount
    user.balance += amount
    user.save()
    print(f">>> PAYMENTS @ paypal_return: Updated user balance with additional {amount}")
    logger.info(f">>> PAYMENTS @ paypal_return: Updated user balance with additional {amount}")

    # TODO Send invoice to user.

    # context = {'post': request.POST, 'get': request.GET}
    # return render(request, 'payments/paypal_return.html', context)
    messages.info(request, _("Thank you for the payment. You should see your balance shortly."))
    return HttpResponseRedirect(reverse("bingo_main:dashboard"))


@csrf_exempt
def paypal_cancel(request):
    # context = {'post': request.POST, 'get': request.GET}
    # return render(request, 'payments/paypal_cancel.html', context)
    messages.info(request, _("Your payment was canceled. Your account balance was not updated."))
    return HttpResponseRedirect(reverse("bingo_main:dashboard"))


# This function will be active only when running online (not localhost)


@receiver(valid_ipn_received)
def payment_confirm(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        # payment was successful
        payment = get_object_or_404(Payment, id=ipn.invoice)
        print(f'Payments: {payment}')
        payment.paid = True
        payment.save()
        user = User.objects.get(pk=payment.user.id)
        user.balance = user.balance + payment.amount
        user.save()


# Credit Cards
#########################
def credit_card_payment(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')

    return render(request, 'payments/credit_card_payment.html')


def payment_success(request):
    context = {}
    return render(request, 'payments/thankyou.html')


def payment_error(request):
    context = {}
    return render(request, 'payments/payment_error.html')
