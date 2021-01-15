import base64, secrets, io
import requests
from PIL import Image
from django.core.files.base import ContentFile
from django.conf import settings

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