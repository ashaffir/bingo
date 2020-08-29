import uuid
from django.db import models
from users.models import User

class Board(models.Model):
    rows = models.IntegerField()
    columns = models.IntegerField()

    def __str__(self):
        return 'Dimensions:' + str(self.rows) + "X" + str(self.columns)

class Album(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    album_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isPublic = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    number_of_images = models.IntegerField(blank=True, null=True)
    pictures = models.JSONField(blank=True, null=True)
    board = models.JSONField(blank=True, null=True)

    # board = models.ForeignKey(Board, null=True, blank=True, on_delete=models.CASCADE )

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

    def __str__(self):
        return str(self.album_id)

class Picture(models.Model):
    image_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.image_id)