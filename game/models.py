import random
import uuid
from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField
from control.models import Category

def picture_image_path(instance, filename):
    return f'pictures/album.{instance.album_id}/{instance.pk}.{filename}'


def prize_image_path(instance, filename):
    return f'games/{instance.game_id}/{filename}'


class Album(models.Model):
    # CATEGORIES = (
    #     ('Movies', 'movies'),
    #     ('Music', 'Music'),
    #     ('Animals', 'animals'),
    #     ('Religion', 'religion'),
    #     ('Politics', 'politics'),
    #     ('Finance', 'finance'),
    #     ('Art', 'art'),
    #     ('Games', 'games'),
    #     ('Other', 'other'),
    # )

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    album_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_public = models.BooleanField(default=False)
    public_approved = models.BooleanField(default=False)
    public_rejected = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    # category = models.CharField(max_length=100,choices=CATEGORIES, blank=True, null=True)
    album_category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)

    number_of_pictures = models.IntegerField(blank=True, null=True)
    pictures = models.JSONField(blank=True, null=True, default=list)
    board = models.JSONField(blank=True, null=True)
    board_size = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

    def __str__(self):
        return str(self.name)

class Picture(models.Model):
    image_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    # album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    album_id = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    remote_id = models.CharField(max_length=100, null=True, blank=True)
    image_file = models.ImageField(upload_to=picture_image_path, blank=True, null=True)
    public = models.BooleanField(default=True)

    def __str__(self):
        return str(self.image_id)


def random_string():
    for i in range(5):
        code = str(random.randint(1001, 9999))
        if not Game.objects.filter(game_id=code).exists():
            return code
    raise ValueError('Too many attempts to generate the code')


class Game(models.Model):

    WINNING_CONDITIONS = (
        ('ROWS', 'ROWS'),
        ('2_ROWS', '2_ROWS'),
        ('FULL_ONLY', 'FULL_ONLY'),
        ('ALL', 'ALL'),
    )

    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    # Game prep
    game_id = models.CharField(max_length=4, null=True, blank=True)
    # game_pk = models.UUIDField(
    #     primary_key=True, default=uuid.uuid4, editable=False)

    album = models.ForeignKey(Album, null=True, blank=True, on_delete=models.CASCADE)
    board_size = models.IntegerField(blank=True, null=True)
    # winning_conditions = models.JSONField(default=list,null=True, blank=True)
    winning_conditions = models.CharField(max_length=10, default='bingo', null=True, blank=True)
    current_winning_conditions = models.CharField(max_length=10, default='bingo', null=True, blank=True)
    # winning_conditions = models.CharField(max_length=10, choices=WINNING_CONDITIONS, default='ALL')
    is_public = models.BooleanField(default=False)
    prizes = models.JSONField(null=True, blank=True)
    max_players = models.IntegerField(default=5)

    auto_join_approval = models.BooleanField(default=False)
    auto_matching = models.BooleanField(default=False) # for drunk users that cannot pay attention - marking resutls automatically


    prize_1_name = models.CharField(max_length=50, null=True, blank=True)
    prize_1_image_file = models.ImageField(upload_to=prize_image_path, blank=True, null=True)
    prize_2_name = models.CharField(max_length=50, null=True, blank=True)
    prize_2_image_file = models.ImageField(upload_to=prize_image_path, blank=True, null=True)
    prize_2_won = models.BooleanField(null=True, blank=True, default=False)
    prize_2_locked = models.BooleanField(null=True, blank=True, default=False)
    prize_3_name = models.CharField(max_length=50, null=True, blank=True)
    prize_3_image_file = models.ImageField(upload_to=prize_image_path, blank=True, null=True)
    prize_3_won = models.BooleanField(null=True, blank=True, default=False)
    prize_3_locked = models.BooleanField(null=True, blank=True, default=False)

    # Start Game
    number_of_players = models.IntegerField(null=True, blank=True, default=0)
    players_list = models.JSONField(blank=True, null=True, default=list)
    game_requested = models.BooleanField(default=False)
    started = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)
    game_in_progress = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    game_cost = models.FloatField(null=True, blank=True, default=0.0)
    pictures_pool = models.JSONField(default=list, null=True, blank=True)
    current_picture = models.ForeignKey(Picture, blank=True, null=True, on_delete=models.CASCADE)
    shown_pictures = models.JSONField(default=list, null=True, blank=True)
    prizes_won = models.JSONField(blank=True, null=True, default=list)

    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.game_id


class Player(models.Model):

    # Player Info
    created = models.DateTimeField(auto_now_add=True)
    player_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=50, null=True, blank=True)

    # Player Game
    game = models.ForeignKey(
        Game, null=True, blank=True, on_delete=models.CASCADE)
    player_game_id = models.CharField(max_length=5, null=True, blank=True)
    approved = models.BooleanField(default=False)
    not_approved = models.BooleanField(default=False)
    board_dict = models.JSONField(null=True, blank=True, default=list)
    # board = models.OneToOneField(Board, null=True, blank=True, on_delete=models.CASCADE)
    board_id = models.CharField(max_length=100, null=True, blank=True)
    winnings = models.JSONField(null=True, blank=True, default=list)
    bingo_shouts = models.IntegerField(null=True, blank=True, default=0)
    active_shout = models.BooleanField(default=False, null=True, blank=True)

    # def __str__(self):
    #     return self.nickname


class Board(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField(null=True, blank=True)
    board_number = models.IntegerField(null=True, blank=True)
    game_id = models.CharField(max_length=30, null=True, blank=True)
    player = models.OneToOneField(
        Player, null=True, blank=True, on_delete=models.CASCADE)
    pictures = ArrayField(
        ArrayField(
            models.CharField(max_length=200, blank=True, null=True),
        ),
        null=True,
        blank=True
    )

    pictures_draw = ArrayField(
        ArrayField(
            models.CharField(max_length=200, blank=True, null=True),
        ),
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.pk)

class DisplayPicture(models.Model):
    image = models.ForeignKey(Picture, null=True, blank=True, on_delete=models.CASCADE)
    game_id = models.IntegerField(null=True, blank=True)
    board = models.ForeignKey(Board, blank=True, null=True, on_delete=models.CASCADE)
    matched = models.BooleanField(default=False)
