import random
import uuid
from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField

class Album(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    album_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    number_of_pictures = models.IntegerField(blank=True, null=True)
    pictures = models.JSONField(blank=True, null=True)
    board = models.JSONField(blank=True, null=True)


    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

    def __str__(self):
        return str(self.name)

class Picture(models.Model):
    image_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    remote_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.image_id)

   
def random_string():
    return str(random.randint(1001, 9999))

class Game(models.Model):

    WINNING_CONDITIONS = (
        ('ROWS', 'ROWS'),
        ('2_ROWS', '2_ROWS'),
        ('FULL_ONLY', 'FULL_ONLY'),
        ('ALL', 'ALL'),
    )

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    # Game prep
    game_id = models.CharField(max_length=4, default=random_string,null=True, blank=True)

    album = models.ForeignKey(Album, null=True, blank=True, on_delete=models.CASCADE)
    board_size = models.IntegerField(blank=True, null=True)
    winning_conditions = models.JSONField(default=list,null=True, blank=True)
    # winning_conditions = models.CharField(max_length=10, choices=WINNING_CONDITIONS, default='ALL')
    is_public = models.BooleanField(default=False)
    prizes = models.JSONField(null=True, blank=True)

    # Start Game
    number_of_players = models.IntegerField(null=True, blank=True)
    players_list = models.JSONField(blank=True, null=True)
    game_requested = models.BooleanField(default=False)
    started = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    game_cost = models.FloatField(null=True, blank=True)
    pictures_pool = models.JSONField(default=list,null=True, blank=True)
    shown_pictures = models.JSONField(default=list,null=True, blank=True)

    is_finished = models.BooleanField(default=False)


    def __str__(self):
        return self.game_id


class Player(models.Model):
    
    # Player Info
    created = models.DateTimeField(auto_now_add=True)
    player_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=50, null=True, blank=True)

    # Player Game
    game = models.ForeignKey(Game, null=True, blank=True, on_delete=models.CASCADE)
    player_game_id = models.CharField(max_length=5, null=True, blank=True)
    approved = models.BooleanField(default=False)
    board_dict = models.JSONField(null=True, blank=True, default=list)
    # board = models.OneToOneField(Board, null=True, blank=True, on_delete=models.CASCADE)
    board_id = models.CharField(max_length=100, null=True, blank=True)
    winnings = models.JSONField(null=True, blank=True, default=list)

    def __str__(self):
        return self.nickname


class Board(models.Model):
    size = models.IntegerField(null=True, blank=True)
    game_id = models.CharField(max_length=30, null=True, blank=True)
    player = models.OneToOneField(Player, null=True, blank=True, on_delete=models.CASCADE)
    pictures = ArrayField(
        ArrayField(
            models.CharField(max_length=100, blank=True, null=True),
        ),
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.pk) 
