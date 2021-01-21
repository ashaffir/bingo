import logging
from django.shortcuts import render, redirect
from django.contrib import messages

from game.models import Album, Picture, Game, Player
from users.utils import send_mail

from .decorators import superuser_required
from users.models import  User
logger = logging.getLogger(__file__)

@superuser_required
def admin_home(request):
    context = {}
    '''
    Settting the newsletter optin option to the ones that are registering without it
    - Select the latest registrar
    - Check if that have opted-in
    - Set their newsletter opt in to True if they have not
    '''
    if request.method == 'POST':
        if 'optin' in request.POST:
            try:
                users = User.objects.filter(newsletter_optin=False) #TODO: implement selection of users on the UI.
                for user in users:
                    user.newsletter_optin = True
                    user.save()
                
                messages.success(request, 'Opt-in option set successfully')
                return redirect(request.META['HTTP_REFERER'])

            except Exception as e:
                print(f">>> ADMINISTRATION @ bulk_set_optin: Failed setting the optin. ERROR: {e} ")
                logger.error(f">>> ADMINISTRATION @ bulk_set_optin: Failed setting the optin. ERROR: {e} ")
                messages.error(request, 'Opt-in set failed!!')
                return redirect(request.META['HTTP_REFERER'])

        else:
            print(f"Wrong button")
            messages.error(request, 'ERROR BUTTON')

        return redirect(request.META['HTTP_REFERER'])
    return render(request, 'administration/admin-home.html')

@superuser_required
def public_albums(request):
    context = {}
    albums = Album.objects.filter(is_public=True, public_approved=False, public_rejected=False)
    albums_images = []
    for album in albums:
        pictures = []
        for pic in album.pictures:
            pictures.append(Picture.objects.get(pk=pic))

        albums_images.append({
            'album_name': album.name, 
            'album_id': str(album.pk), 
            'album_user': str(album.user), 
            'board_size': album.board_size, 
            'pictures': pictures
            })

    context['albums_images'] = albums_images
    context['albums'] = albums

    if request.method == 'POST':
        if 'approve_album' in request.POST:
            album_id = request.POST.get('approve_album')
            print(f"APPROVING ALBUM: {album_id}")
            album = Album.objects.get(album_id=album_id)
            album_user = album.user
            album.public_approved = True
            album.save()

            # Send update email to the user about the upproval
            try:
                subject = "Album pictures approved"
                title = "Your album was approved by the admin"
                content = f'''
                Congratulations, the images in your album: ID {album.album_id}, name {album.name} was approved for public display.
                '''
                message = {
                    'title': title,
                    'email': album_user.email,
                    'content': content,
                }

                send_mail(subject, email_template_name=None, attachement='',
                            context=message, to_email=[
                                album_user.email],
                            html_email_template_name='bingo_main/emails/user_update_email.html')
            except Exception as e:
                logger.error(
                    f'>>> ADMINISTRATION@admin_home: Failed sending email updating the user on an approved album. ERROR: {e}')
                print(
                    f'>>> ADMINISTRATION@admin_home: Failed sending email updating the user on an approved album. ERROR: {e}')

            messages.success(request, f'Album approved successfuly!!')
            return redirect('administration:admin_home')
        
        elif 'reject_album' in request.POST:
            album_id = request.POST.get('reject_album')
            print(f">>> ADMINISTRATION@admin_home: rejecting {album_id}")
            logger.info(f">>> ADMINISTRATION@admin_home: rejecting {album_id}")
            album = Album.objects.get(album_id=album_id)
            album_user = album.user
            album.public_rejected = True
            album.save()

            # Send update email to the user about the upproval
            try:
                subject = "Album pictures rejected"
                title = "Your album was rejected by the admin"
                content = f'''
                The images in your album: ID {album.album_id}, name {album.name} was not approved for public display.
                Please make sure you follow Polybingo restrictions about publishing pictures on the public page.
                Please contact our support if you have any question.
                '''
                message = {
                    'title': title,
                    'email': album_user.email,
                    'content': content,
                }

                send_mail(subject, email_template_name=None, attachement='',
                            context=message, to_email=[
                                album_user.email],
                            html_email_template_name='bingo_main/emails/user_update_email.html')
            except Exception as e:
                logger.error(
                    f'>>> ADMINISTRATION@admin_home: Failed sending email ot the user updating on a rejected album. ERROR: {e}')
                print(
                    f'>>> ADMINISTRATION@admin_home: Failed sending email ot the user updating on a rejected album. ERROR: {e}')

            messages.success(request, f'Album rejected successfuly!!')
            return redirect('administration:public_albums')

    return render(request, 'administration/public-albums.html', context)

def contact_us_requests(request):
    context = {}
    return render(request, 'administration/contact-us-requests.html')
