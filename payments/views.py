import requests
import stripe
from django.shortcuts import render, get_object_or_404, reverse, redirect, resolve_url
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.dispatch import receiver
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated


from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import valid_ipn_received

from .models import Payment
from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY 

# Generate an invoice
# INVOICE = "unique_invoice_00001"

@login_required
def paypal_payment(request, amount=0.0):
    deposit_id = request.session.get('order_id')
    context = {}
    host = request.get_host()
    host = request.user

    invoice = Payment.objects.create(
        amount = amount,
        user = host
    )

    # PayPal Payments
    #################
    paypal_dict = {
        "business" : settings.PAYPAL_RECEIVER_EMAIL,
        "amount" : amount,
        "currency" : settings.CURRENCY,
        "locale": 'en_US',
        "style": {
            "size": 'medium',
            "color": 'blue',
            "shape": 'pill',
            "label": 'Deposit',
            "tagline": 'true'
            },
        "item_name" : "Deposit",
        "invoice" : invoice.id,
        "notify_url" : 'http://{}{}'.format(host, reverse('payments:paypal-ipn')),
        "return_url" : f"http://{host}/payments/paypal_return/",
        "cancel_url" : f"http://{host}/payments/paypal_cancel/"
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

    context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY

    context['form'] = form
    context['amount'] = amount
    # return render(request, 'payments/payment.html', context)
    return render(request, 'payments/paypal_payment.html', context)


@login_required
def stripe_payment(request, amount=0.0):
    context = {}
    context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
    context['amount'] = amount
    return render(request, 'payments/stripe_payment.html', context)

@login_required
def charge(request):
    if request.method == 'POST':
        print('Charge info:', request.POST)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        user = User.objects.get(pk=request.user.pk)
        name = user.name
        email = user.username
        amount = float(request.POST.get('amount'))
        try:
            if not user.stripe_customer_key:
                customer = stripe.Customer.create(
                        name = name,
                        email = email,
                        source = request.POST['stripeToken']
                    )
                
                stripe.Charge.create(
                    customer=customer,
                    amount=int(amount * 100),
                    currency="eur", # TODO: make dynamic according to browser language
                    description="PolyBingo funds deposit",
                    )

                # Adding stripe customer key to the user
                user.stripe_customer_key = customer.id
            else:
                stripe.Charge.create(
                    customer=user.stripe_customer_key,
                    amount=int(amount * 100),
                    currency="usd", # TODO: make dynamic according to browser language
                    description="PolyBingo funds deposit",
                    )
        except Exception as e:
                print('Failed to charge Stripe account')

    # Adding the amount to the user's balance
    user.balance = user.balance + amount
    user.save()


    return redirect(reverse('payments:success', args=[amount]))

def successMsg(request, args):
	amount = args
	return render(request, 'payments/success.html', {'amount':amount})


@login_required
def deposits(request):
    context = {}
    if request.method == 'POST':
        if 'deposit_amount' in request.POST:
            amount = request.POST.get('deposit_amount')
            if amount is not '':
                return HttpResponseRedirect(reverse('payment', args=[amount]))
            else:
                messages.error(request, 'Please enter an amount, or pick pf the predefined amounts.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    return render(request, 'payments/deposits.html', context)

@csrf_exempt
def paypal_return(request):
    context = {'post':request.POST, 'get':request.GET}
    return render(request, 'payments/paypal_return.html', context)

@csrf_exempt
def paypal_cancel(request):
    context = {'post':request.POST, 'get':request.GET}
    return render(request,'payments/paypal_cancel.html', context)

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


## Credit Cards
#########################
def credit_card_payment(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')

    return render(request,'payments/credit_card_payment.html')

def payment_success(request):
    context = {}
    return render(request, 'payments/thankyou.html')

def payment_error(request):
    context = {}
    return render(request, 'payments/payment_error.html')

    