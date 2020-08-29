from django.shortcuts import render
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action


from .models import Album, Picture
from . import serializers

@api_view(['GET','POST',],)
@permission_classes((IsAuthenticated,))
def pictures(request):
    if request.method == 'GET':
        data = {}
        album = request.data['album_id']
        pictures = Picture.objects.filter(album=album).values()
        pictures_list = []
        for picture in pictures:
            print(f'PICTURE: {picture}')
            serializer = serializers.PicturesSerializer(picture, data=request.data)
            if serializer.is_valid():
                pictures_list.append(picture)
            else:
                print(f'Failed picture serializing. ERROR: {serializer.errors}')
        data['pictures'] = pictures_list
        data['response'] = f'Picture for album: {album}'
    else:
        return Response(status.HTTP_400_BAD_REQUEST)
    if len(pictures_list) == 0:
        return Response(data='No Pictures', status=status.HTTP_200_OK)
    else:
        return Response(data)

@api_view(['POST', 'GET'],)
@permission_classes((IsAuthenticated,))
def albums(request):
    '''
    Retreive albums: either public ones or per user
    API endpoints: 
    /api/game/albums/ for particular user (the one that is logged in)
    /api/game/albums/?albums=all for all public

    Create 
    '''
    data = {}
    if request.method == 'GET':
        query = request.GET.get('albums')
        if query == 'public':
            public_albums = Album.objects.filter(isPublic=True)
            albums_list = []
            for album in public_albums:
                serializer = serializers.AlbumSerializer(album, data=request.data) 
                if serializer.is_valid():
                    albums_list.append(serializer.data)
                else:
                    print(f'Failed picture serializing. ERROR: {serializer.errors}')

            data['response'] = 'Public albums'
        else:
            albums = Album.objects.filter(Q(user=request.user))
            albums_list = []
            for album in albums:
                serializer = serializers.AlbumSerializer(album, data=request.data) 
                if serializer.is_valid():
                    albums_list.append(serializer.data)
            data['response'] = f'Albums for user: {request.user}'

            # print(f'ERROR GETTNIG ALL ALBUMS')
            # data = serializer.errors
        data['albums'] = albums_list
        return Response(data)

    # Create new album
    elif request.method == 'POST':
        data = {}
        print(f'DATA: {request.data}')
        album_name = request.data['name']
        user = request.user
        pictures = request.data['pictures']
        board = request.data['board']
        
        album = Album()
        album.name = album_name
        album.user = user
        album.pictures = pictures
        album.board = board
        album.number_of_images = len(pictures[0])
        album.save()
        print(f'IMAGES: {pictures[0]}')

        serializer = serializers.AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            data = serializer.data
        else:
            return Response('ERROR SERIALIZING NEW ALBUM')

        # Card:{
        # Row:nubmer,
        # Column: number,
        # isEmptyCenter: boolean

        return Response(data)

    return Response(status.HTTP_400_BAD_REQUEST)
 

    # return Response(data='Images loaded', status=status.HTTP_200_OK)

################ NOT USED ###################
class UserAlbumsView(viewsets.ModelViewSet):
    serializer_class = serializers.AlbumSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)

    # queryset = Order.objects.all()
    @action(methods=['POST', ], detail=False)
    def get_queryset(self, *args, **kwargs):
        # queryset_list = Album.objects.all()
        user = self.request.user
        queryset_list = queryset_list.filter(Q(user=user))
        print(f'USER {user}  Albums: {queryset_list}')

        return queryset_list

