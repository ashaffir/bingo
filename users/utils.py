import sys
import logging
from django.template import RequestContext, TemplateDoesNotExist
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__file__)


def send_mail(subject, email_template_name,attachement,
              context, to_email, html_email_template_name=None, request=None, from_email=None):
    """
    Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
    """

    print(f'''
    subject: {subject}
    html email template name: {html_email_template_name}
    context: {context}
    to email: {to_email}
    request: {request}
    from email: {from_email}
    ''')
    ctx_dict = {}
    if request is not None:
        ctx_dict = RequestContext(request, ctx_dict)
    # update ctx_dict after RequestContext is created
    # because template context processors
    # can overwrite some of the values like user
    # if django.contrib.auth.context_processors.auth is used
    if context:
        ctx_dict.update(context)

    # Email subject *must not* contain newlines
    from_email = from_email or getattr(settings, 'DEFAULT_FROM_EMAIL')
    if email_template_name:
        message_txt = render_to_string(email_template_name,ctx_dict)

        email_message = EmailMultiAlternatives(subject, message_txt,from_email, to_email)
    
    else:
        try:
            message_html = render_to_string(
                html_email_template_name, ctx_dict)
            email_message = EmailMultiAlternatives(subject, message_html,
                                                   from_email, to_email)
            email_message.content_subtype = 'html'
            if attachement != '':
                try:
                    email_message.attach_file(attachement)
                except Exception as e:
                    print(f">>> USERS UTILS @send_mail: Failed to attach attachement. ERROR: {e}")
                    logger.error(f">>> USERS UTILS @send_mail: Failed to attach attachement. ERROR: {e}")
        except TemplateDoesNotExist:
            pass


    try:
        email_message.send()
        logger.info(f'>>> USERS UTILS @ send_mail: Mail sent to {to_email}')
    except Exception as e:
        if settings.DEBUG:
            print(f'ERROR: email not sent (utilities.py). Reason: {e}')
            print(sys.exc_info())
        else:
            logger.error(f'ERROR: email not sent (utilities.py). Reason: {e}')
