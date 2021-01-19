import os
import requests
import stripe
import logging
import platform
from io import BytesIO
from django.shortcuts import render, get_object_or_404, reverse, redirect, resolve_url
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.dispatch import receiver
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.template.loader import get_template
from django.views.generic import ListView
from django.contrib.staticfiles import finders
from django.core.files import File

from xhtml2pdf import pisa

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated


from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import valid_ipn_received

from .models import Payment, Coupon
from users.models import User
from users.utils import send_mail
from bingo_main.models import ContentPage

from administration.decorators import superuser_required

logger = logging.getLogger(__file__)

stripe.api_key = settings.STRIPE_SECRET_KEY

# Generate an invoice
# INVOICE = "unique_invoice_00001"

# class UserListView(ListView):
#     model = User
#     template_name = 'payments/users_invoices.html'

def invoice_html(request):
    return render(request, 'payments/invoice.html')

def user_render_pdf_view(request, *args, **kwargs):
    user_pk = kwargs.get('pk')
    user = get_object_or_404(User, pk=user_pk)
    
    template_path = 'payments/invoice.html'
    context = {'user': user}

    # Create Django response object and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # To download the PDF run:
    # response['Content-Disposition'] = 'attachement; filename="invoice.pdf"'

    # To display it:
    response['Content-Disposition'] = 'filename="user_info.pdf"'

     #find the templage and render it
    template = get_template(template_path)
    html = template.render(context)

    #Create the PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # If error show this
    if pisa_status.err:
        return HttpResponse('Error creating PDF <pre>' + html + '</pre>')
    
    return response


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_invoice_pdf(payment_id):
        
    if platform.system() == 'Darwin':  # MAC
        current_site = 'http://127.0.0.1:8000' if settings.DEBUG else settings.DOMAIN_PROD
    else:
        current_site = settings.DOMAIN_PROD

    payment = Payment.objects.get(id=payment_id)
    context = {'payment': payment}

    pdf = render_to_pdf('payments/invoice.html', context)
    filename = f"PI0000{payment.id}.pdf"
    payment.invoice_pdf.save(filename, File(BytesIO(pdf.content)))
    return payment.invoice_pdf.url

# def render_pdf_view(request):
#     payment = Payment.objects.get(pk=1)
#     template_path = 'payments/invoice.html'
#     context = {'payment': payment}

#     # Create Django response object and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')


#     pdf = render_to_pdf(template_path, context)
    
#     filename = f"YourPDF_Order{payment.invoice_slug}.pdf"
#     payment.invoice_pdf.save(filename, File(BytesIO(pdf.content)))
    
#     # To directly download the PDF run:
#     # response['Content-Disposition'] = 'attachement; filename="invoice.pdf"'

#     # To display it:
#     response['Content-Disposition'] = 'filename="invoice.pdf"'

#      #find the templage and render it
#     template = get_template(template_path)
#     html = template.render(context)

#     #Create the PDF
#     pisa_status = pisa.CreatePDF(html, dest=response)

#     # If error show this
#     if pisa_status.err:
#         return HttpResponse('Error creating PDF <pre>' + html + '</pre>')

#     return response

def check_coupon(coupon):
    try:
        coupons = Coupon.objects.filter(active=True)
        coupons_ids = []
        for c in coupons:
            coupons_ids.append(c.coupon_id)

        if coupon in coupons_ids:
            discount = Coupon.objects.get(coupon_id=coupon).discount
            return discount
        else:
            return 0.0
    except Exception as e:
        print(f'>>> PAYMENTS @ check_coupon: No coupon found. E: {e}')
        logger.info(f'>>> PAYMENTS @ check_coupon: No coupon found. E: {e}')
        return 0.0

@login_required
def payment(request, amount=0.0, coupon=''):
    print(f'>>> PAYMENTS @ payment: Amount {amount}')
    logger.info(f'>>> PAYMENTS @ payment: Amount {amount}')
    deposit_id = request.session.get('payment_id')
    context = {}
    context['site_recaptcha'] = settings.RECAPTCHA_PUBLIC_KEY

    host = request.get_host()
    user = request.user

    discount = check_coupon(coupon)

    if discount == 1.0:
        free_amount = Coupon.objects.get(coupon_id=coupon).free_amount
        user.balance += free_amount
        user.save()
        messages.success(request, _(f"Your account was sucessfully credited with $" + str(free_amount)))
        return redirect('bingo_main:dashboard')

    total_charge = amount * (1 - discount)
    
    payment = Payment.objects.create(
        amount=amount,
        total_charge=total_charge,
        user=user,
        discount=discount
    )

    ipn_url = (
        # settings.PAYPAL_IPN_URL or
        'http://{}{}'.format(host, reverse('payments:paypal-ipn'))
    )
    # PayPal Payments
    #################
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": total_charge ,
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
        "invoice": payment.id,
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
    context['amount'] = total_charge
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


        # Generate and send invoice to the user
        payment = Payment.objects.filter(user=user).last()
        payment.payment_type = 'Credit Card'
        payment.save()

        try:
            invoice_sub_path = generate_invoice_pdf(payment.pk)
            invoice_path = str(settings.BASE_DIR) + invoice_sub_path
            print(f">>> PAYMENTS @ charge: Invoice path: {invoice_path}")
            logger.info(f">>> PAYMENTS @ charge: Invoice path: {invoice_path}")
        except Exception as e:
            print(f">>> PAYMENTS @ charge: Falied saving the invoice PDF file. ERROR: {e}")
            logging.error(f">>> PAYMENTS @ charge: Falied saving the invoice PDF file. ERROR: {e}")

            #TODO: write an "Update Admin" routin to send emails to admin every break

        try:
            email_message = ContentPage.objects.get(name='invoice_email')
            subject = _(f"New Invoice From Polybingo - PI0000" + str(payment.pk))
            title = email_message.title
            content = email_message.content
            
            message = {
                'message': content
            }

            send_mail(subject, 
                        email_template_name=None,
                        attachement=invoice_path,
                        context=message, to_email=[user.email],
                        html_email_template_name='bingo_main/emails/user_email.html')
        except Exception as e:
            logger.error(f'>>> PAYMENTS @ charge: Failed sending admin email with invoice. ERROR: {e}')
            print(f'>>> PAYMENTS @ charge: Failed sending admin email with invoice. ERROR: {e}')


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
                messages.error(request, _('Please enter an amount, or pick one of the predefined amounts.'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'payments/deposits.html', context)


@csrf_exempt
def paypal_return(request):
    user = request.user

    if settings.DEBUG:
        payment = Payment.objects.filter(user=user).last()
        amount = payment.amount
        user.balance += amount
        user.save()
    
        print(f">>> PAYMENTS @ paypal_return: Updated user balance with additional {amount}")
        logger.info(f">>> PAYMENTS @ paypal_return: Updated user balance with additional {amount}")
    
    payment.payment_type = 'PayPal'
    payment.save()


    # Generate and send invoice to the user
    try:
        invoice_sub_path = generate_invoice_pdf(payment.pk)
        invoice_path = str(settings.BASE_DIR) + invoice_sub_path
        print(f">>> PAYMENTS @ paypal_return: Invoice path: {invoice_path}")
        logger.info(f">>> PAYMENTS @ paypal_return: Invoice path: {invoice_path}")
    except Exception as e:
        print(f">>> PAYMENTS @ paypal_return: Falied saving the invoice PDF file. ERROR: {e}")
        logging.error(f">>> PAYMENTS @ paypal_return: Falied saving the invoice PDF file. ERROR: {e}")

    try:
        email_message = ContentPage.objects.get(name='invoice_email')
        subject = _(f"New Invoice From Polybingo - PI0000" + str(payment.pk))
        title = email_message.title
        content = email_message.content
        
        message = {
            'message': content,
        }

        send_mail(subject, 
                    email_template_name=None,
                    attachement=invoice_path,
                    context=message, to_email=[user.email],
                    html_email_template_name='bingo_main/emails/user_email.html')
    except Exception as e:
        logger.error(f'>>> PAYMENTS @ paypal_return: Failed sending admin email with invoice. ERROR: {e}')
        print(f'>>> PAYMENTS @ paypal_return: Failed sending admin email with invoice. ERROR: {e}')


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
        print(f'>>> Payments @ payment_confirm : Deposit amount {payment}')
        logger.info(f'>>> Payments @ payment_confirm : Deposit amount {payment}')
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
