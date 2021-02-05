import stripe
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings

from users.models import User
from .models import Customer
from .forms import CustomSignupForm

stripe.api_key = settings.STRIPE_SECRET_KEY

def plans(request):
    return render(request, 'membership/plans.html')

@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False
        else:
            customer.membership = True
        customer.cancel_at_period_end = subscription.cancel_at_period_end
        customer.save()
    return HttpResponse('completed')
    
@login_required
def membership_settings(request):
    context = {}
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    
    context['membership'] = membership
    context['cancel_at_period_end'] = cancel_at_period_end

    return render(request, 'membership/membership_settings.html',  context)


def join(request):
    return render(request, 'membership/plans.html')


def success(request):
    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'],)
        customer = Customer()
        print(f"USER: {request.user}")
        customer.user = request.user
        customer.stripeid = session.customer
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = session.subscription
        customer.save()
    return render(request, 'membership/success.html')


def cancel(request):
    return render(request, 'membership/cancel.html')

@login_required
def make_payment(request):
    context = {}
    return render(request, "membership/make-payment.html", context)

@login_required
def checkout(request):
    context = {}
    context['dashboard'] = True
    try:
        if request.user.customer.membership:
            return redirect('membership:membership_settings')
    except Customer.DoesNotExist:
        pass

    if request.method == 'POST':
        pass
    else:
        membership = 'monthly'
        final_dollar = 5
        membership_id = 'price_1IE9eeEkukXQn9UkFRvQ4mJ2' if settings.DEBUG else 'price_1IE8mLEkukXQn9UkP0Cl4xP2'
        if request.method == 'GET' and 'membership' in request.GET:
            if request.GET['membership'] == 'yearly':
                membership = 'yearly'
                membership_id = 'price_1IE9eeEkukXQn9UkopY2ggfE' if settings.DEBUG else 'price_1IE8mKEkukXQn9UkNUS8R0iC'
                final_dollar = 50

        # Create Strip Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email = request.user.email,
            line_items=[{
                'price': membership_id,
                'quantity': 1,
            }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url='http://127.0.0.1:8030/membership/success/',
            cancel_url='http://127.0.0.1:8030/membership/cancel',
        )

        print(f"STRIP SESSION: {session}")

        context['final_dollar'] = final_dollar
        context['session_id'] = session.id

        return render(request, 'membership/checkout.html', context)

