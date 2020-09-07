import random
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

    def __str__(self):
        return str(self.image_id)

   
def random_string():
    return str(random.randint(1001, 9999))

class Game(models.Model):

    WINNING_CONDITIONS = (
        ('ROWS', 'ROWS'),
        ('COLUMNS', 'COLUMNS'),
        ('FULL_ONLY', 'FULL_ONLY'),
        ('ALL', 'ALL'),
    )
    # Game prep
    game_id = models.CharField(max_length=4, default=random_string)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    album_id = models.ForeignKey(Album, null=True, blank=True, on_delete=models.CASCADE)
    winning_conditions = models.CharField(max_length=10, choices=WINNING_CONDITIONS, default='ALL')
    is_public = models.BooleanField(default=False)
    number_of_players = models.IntegerField(null=True, blank=True)
    players_list = models.JSONField(blank=True, null=True)

    # Start Game
    started = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    game_cost = models.FloatField(null=True, blank=True)
    shown_pictures = models.JSONField(null=True, blank=True)

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
    board = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.nickname
