import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from .forms import ContactForm
from .models import ContentPage

logger = logging.getLogger(__file__)

def bingo_main(request):
    context = {}
    return render(request, 'bingo_main/index.html')

def bingo_main_register(request):
    context = {}
    return render(request, 'bingo_main/register.html')

def bingo_main_login(request):
    context = {}
    return render(request, 'bingo_main/login.html')

def about(request):
    context = {}
    try:
        about = ContentPage.objects.get(name='about')
        context['about'] = about
    except Exception as e:
        messages.error(request, 'This page content is not ready')
        logger.error('>>> Bingo main: not content for the About section')
    return render(request, 'bingo_main/about.html', context)

def terms(request):
    context = {}
    try:
        terms = ContentPage.objects.get(name='terms')
        context['terms'] = terms
    except Exception as e:
        messages.error(request, 'This page content is not ready')
        logger.error('>>> Bingo main: not content for the Terms section')
    return render(request, 'bingo_main/terms.html', context)

def pricing(request):
    context = {}
    try:
        terms = ContentPage.objects.get(name='pricing')
        context['pricing'] = pricing
    except Exception as e:
        messages.error(request, 'This page content is not ready')
        logger.error('>>> Bingo main: not content for the pricing section')
    return render(request, 'bingo_main/pricing.html', context)

def why_and_how(request):
    context = {}
    try:
        terms = ContentPage.objects.get(name='why_and_how')
        context['why_and_how'] = why_and_how
    except Exception as e:
        messages.error(request, 'This page content is not ready')
        logger.error('>>> Bingo main: not content for the why_and_how section')
    return render(request, 'bingo_main/why_and_how.html', context)

def contact(request):
    context = {}
    print('>>> SENDING CONTACT')
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message was sent. We will be in touch soon')
            # return redirect(request.META['HTTP_REFERER'])
            return redirect('bingo_main:bingo_main')
        else:
            messages.error(request, 'Your message was not sent. Please try again later')
            logger.error('>> BING MAIN: Error sending contact us message')
            return redirect('bingo_main:bingo_main')

    return render(request, 'bingo_main/contact.html')

@login_required
def dashboard(request):
    context = {}
    return render(request, 'bingo_main/dashboard/index.html')

@login_required(login_url='bingo_main:bingo_main_login')
def create_bingo(request):
    context = {}

    if request.method == 'POST':
        if 'updateProfile' in request.POST:
            print(f'UPDATE: {request.POST}')

    return render(request, 'bingo_main/dashboard/create-bingo.html')

@login_required
def my_bingos(request):
    context = {}
    return render(request, 'bingo_main/dashboard/my-bingos.html')

@login_required
def bingo(request):
    context = {}
    return render(request, 'bingo_main/bingo.html')

@login_required
def add_money(request):
    context = {}
    return render(request, 'bingo_main/dashboard/add-money.html')

@login_required
def logout_view(request):
    context = {}
    logout(request)
    return redirect('bingo_main:bingo_main')


def game_index(request):
    context = {}
    logout(request)
    return render(request, 'bingo_main/broadcast/index.html')

def game(request, game_id):
    context = {}
    logout(request)
    return render(request, 'bingo_main/broadcast/game.html')

def check_card(request):
    context = {}
    logout(request)
    return render(request, 'bingo_main/broadcast/checkCard.html')



def handler404(request, exception, template_name="404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response

def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)