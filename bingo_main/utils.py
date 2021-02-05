import base64, secrets, io
import requests
import json
import logging
from PIL import Image
from django.core.files.base import ContentFile
from django.conf import settings
from users.utils import send_mail

logger = logging.getLogger(__file__)


def alert_admin(alert, location):
    # Send email to admin
    try:
        subject = "Alert from Polybingo!"

        message = {
            'title': location,
            'alert': True,
            'content': alert,
        }

        send_mail(subject, email_template_name=None, attachement='',
                    context=message, to_email=[
                        settings.ADMIN_EMAIL],
                    html_email_template_name='bingo_main/emails/admin_email.html')
        return True
    
    except Exception as e:
        logger.error(
            f'>>> BINGO MAIN: Failed sending admin email updating on a new contact from homepage. ERROR: {e}')
        print(
            f'>>> BINGO MAIN: Failed sending admin email updating on a new contact from homepage. ERROR: {e}')
        return False

def get_image_from_data_url( data_url, resize=True, base_width=600 ):

    # getting the file format and the necessary dataURl for the file
    _format, _dataurl       = data_url.split(';base64,')
    # file name and extension
    _filename, _extension   = secrets.token_hex(20), _format.split('/')[-1]

    # generating the contents of the file
    file = ContentFile( base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")

    # resizing the image, reducing quality and size
    if resize:

        # opening the file with the pillow
        image = Image.open(file)
        # using BytesIO to rewrite the new content without using the filesystem
        image_io = io.BytesIO()

        # resize
        w_percent    = (base_width/float(image.size[0]))
        h_size       = int((float(image.size[1])*float(w_percent)))
        image        = image.resize((base_width,h_size), Image.ANTIALIAS)

        # save resized image
        image.save(image_io, format=_extension)

        # generating the content of the new image
        file = ContentFile( image_io.getvalue(), name=f"{_filename}.{_extension}" )

    # file and filename
    return file, ( _filename, _extension )

def get_image_and_thumbnail_from_data_url( data_url, resize=True, base_width=600):
    #
    file, filename = get_image_from_data_url(data_url, resize, base_width)

    #
    thumbnail = Image.open(file)

    #
    thumbnail_io = io.BytesIO()
    thumbnail.thumbnail((128,128), Image.ANTIALIAS)
    thumbnail.save(thumbnail_io, format=filename[1])

    # thumbnail image
    thumbnail = ContentFile( 
        thumbnail_io.getvalue(), 
        name=f"{filename[0]}.thumbnail.{filename[1]}"
    )

    return file, thumbnail


def check_captcha(request):
    client_key = request.POST['g-recaptcha-response']
    secret_key = settings.RECAPTCHA_PRIVATE_KEY

    captcha_data = {
        'secret':secret_key,
        'response':client_key
    }

    r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=captcha_data)
    response = json.loads(r.text)
    verify = response['success']
    return verify



def clear_session(request):
    session_keys = ['new_album', 'album_update']
    
    try:
        for key in session_keys:
            del request.session[key]
    except KeyError:
        return

    return


def clear_session_key(request, session_key):
    try:
        del request.session[session_key]
    except KeyError:
        return

    return


def delete_session(request):
    try:
        del request.session['user']
        del request.session['password']
    except KeyError:
        pass
    
    return render(request, 'bingo_main:bingo_main')