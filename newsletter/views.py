import datetime
import logging
import platform
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from users.models import User
from users.utils import send_mail
from .forms import NewsletterForm
from .models import Newsletter

logger = logging.getLogger(__file__)


def newsletter_admin(request):
    context = {}
    newsletters = Newsletter.objects.all()
    context['newsletters'] = newsletters
    if request.method == 'POST':
        if 'selectNewsletterButton' in request.POST:
            newsletter = Newsletter.objects.get(pk=request.POST.get('newsletterSelect'))
            subject = newsletter.subject

            # message = {
            #     'title_1': newsletter.title_1,
            #     'content_1': newsletter.content_1,
            #     'button_text':newsletter.button_text,
            #     'button_link':newsletter.button_link,
            #     'title_2': newsletter.title_2,
            #     'content_2': newsletter.content_2,
            #     'image'
            #     'title_3': newsletter.title_3,
            #     'content_3': newsletter.content_3,
            # }

            context['message'] = newsletter
            context['admin'] = True
            context['recipients_type'] = newsletter.recipients_type
            context['lang'] = 'he' if newsletter.language == 'Hebrew' else 'en'
            try:
                context['user'] = User.objects.get(pk=newsletter.recipients[0])
            except:
                print('No receipients')

            return render(request, 'newsletter/newsletter.html', context)

        elif 'sendTest' in request.POST:
            if platform.system() == 'Darwin': # MAC
                current_site = 'http://127.0.0.1:8030' if settings.DEBUG else settings.DOMAIN_PROD
            else:
                current_site = settings.DOMAIN_PROD

            try:
                newsletter = Newsletter.objects.get(pk=request.POST.get('newsletterSelect'))
            except Exception as e:
                messages.error(request, 'No newsletter template selected')
                return redirect(request.META['HTTP_REFERER'])
                

            test_recipient = request.POST.get('testEmail')            
            user = User.objects.get(is_superuser=True)
                
            subject = newsletter.subject

            # message = {
            #     'title_1':  newsletter.title_1,
            #     'content_1':  newsletter.content_1,
            #     'title_2':  newsletter.title_2,
            #     'content_2':  newsletter.content_2,
            #     'title_3':  newsletter.title_3,
            #     'content_3':  newsletter.content_3,
            #     'button_text': newsletter.button_text,
            #     'button_link': newsletter.button_link,
            #     'lang': 'he' if newsletter.language == 'Hebrew' else 'en',
            #     'user': user,
            #     'domain': current_site
            # }

            context['message'] = newsletter
            context['lang'] = 'he' if newsletter.language == 'Hebrew' else 'en'
            context['user'] = user
            context['domain'] = current_site

            try:
                send_mail(subject, email_template_name=None,attachement='',
                    context=message, to_email=[test_recipient],
                    html_email_template_name='newsletter/newsletter.html')
                messages.success(request, f"TEST Newsletter sent successfully to {test_recipient}")
                
            except Exception as e:
                logging.error(f">>> NEWSLETTER: Failed test email on user. ERROR: {e}")
                messages.error(request,f">>> NEWSLETTER: Failed test email on user. ERROR: {e}")
                print(f">>> NEWSLETTER: Failed test email on user. ERROR: {e}")


        elif 'sendNewsLetter' in request.POST:
            if platform.system() == 'Darwin': # MAC
                current_site = 'http://127.0.0.1:8030' if settings.DEBUG else settings.DOMAIN_PROD
            else:
                current_site = settings.DOMAIN_PROD

            try:
                newsletter = Newsletter.objects.get(pk=request.POST.get('newsletterSelect'))
            except Exception as e:
                messages.error(request, 'No newsletter template selected')
                return redirect(request.META['HTTP_REFERER'])
            
            for user_id in newsletter.recipients:
                user = User.objects.get(pk=user_id)
                
                subject = newsletter.subject

                # message = {
                #     'title_1':  newsletter.title_1,
                #     'content_1':  newsletter.content_1,
                #     'title_2':  newsletter.title_2,
                #     'content_2':  newsletter.content_2,
                #     'title_3':  newsletter.title_3,
                #     'content_3':  newsletter.content_3,
                #     'button_text': newsletter.button_text,
                #     'button_link': newsletter.button_link,
                #     'lang': 'he' if newsletter.language == 'Hebrew' else 'en',
                #     'user': user,
                #     'domain': current_site
                # }

                context['message'] = newsletter
                context['lang'] = 'he' if newsletter.language == 'Hebrew' else 'en'
                context['user'] = user
                context['domain'] = current_site

                try:
                    send_mail(subject, email_template_name=None,attachement='',
                        context=message, to_email=[user.email],
                        html_email_template_name='newsletter/newsletter.html')
                except Exception as e:
                    logging.error(f">>> NEWSLETTER: Failed email on user {user}. ERROR: {e}")
                    messages.error(request, f">>> NEWSLETTER: Failed email on user {user}. ERROR: {e}")
                    print(f">>> NEWSLETTER: Failed email on user {user}. ERROR: {e}")

            newsletter.sent = True
            newsletter.sent_date = datetime.datetime.now()
            newsletter.save()
            messages.success(request, f"Newsletter sent successfully to {len(newsletter.recipients)} users")
        return redirect('newsletter:newsletter_admin')
    
    return render(request, 'newsletter/newsletter_admin.html', context)

def newsletter_form(request):
    # form = NewsletterForm()
    context = {}

    if request.method == 'POST':
        newsletter = Newsletter()
        # Collect relevant subscribers
        recipients = []
        recipients.extend(User.objects.filter(newsletter_optin=True))
        newsletter.recipients_type = 'all'


        newsletter.name = request.POST.get('newsletter_name')
        newsletter.subject = request.POST.get('subject')
        newsletter.title_1 = request.POST.get('title_1')
        newsletter.content_1 = request.POST.get('content_1')
        newsletter.title_2 = request.POST.get('title_2')
        newsletter.content_2 = request.POST.get('content_2')
        newsletter.title_3 = request.POST.get('title_3')
        newsletter.content_3 = request.POST.get('content_3')
        newsletter.button_text =request.POST.get('button_text')
        newsletter.button_link =request.POST.get('button_link')

        for user in recipients:
            newsletter.recipients.append(user.pk)

        newsletter.recipients_count = len(recipients)
        newsletter.save()
        context['admin'] = True
        return render(request, 'newsletter/newsletter.html', context)
        
    return render(request, 'newsletter/newsletter_form.html', context)

def newsletter_test(request):
    context = {}
    return render(request, 'newsletter/newsletter.html', context)


def unsubscribe(request, user_id):
    context = {}
    try:
        unsubscribe_user = User.objects.get(pk=user_id)
        unsubscribe_user.newsletter_optin = False
        unsubscribe_user.save()
        context['user'] = unsubscribe_user
    except Exception as e:
        logger.info('No user to unsubscribe')

    return render(request, 'newsletter/unsubscribe.html', context)


def re_subscribe(request, user_id):
    context = {}
    try:
        subscribe_user = User.objects.get(pk=user_id)
        subscribe_user.newsletter_optin = True
        subscribe_user.save()
        context['user'] = subscribe_user
    except Exception as e:
        logger.info('No user to subscribe')

    messages.success(request, f'You were re-subscribed to our newsletters')
    return render(request, 'bingo_main/index.html', context)

def landing_page(request):
    context = {}
    return render(request, 'newsletter/landing_pages/landing_page.html', context)