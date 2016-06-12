from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from foosball.games.utils import random_colour
from foosball.users.models import User


class Table(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name=_("name"))
    description = models.TextField(blank=True, verbose_name=_("description"))

    def __str__(self):
        return self.name


class Game(TimeStampedModel):
    created_by = models.ForeignKey(
        User, related_name="games_created", editable=False, null=True, verbose_name=_("created by")
    )
    modified_by = models.ForeignKey(
        User, related_name="games_modified", editable=False, null=True, verbose_name=_("modified by")
    )

    played_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("played at"),
        help_text=_("Time when the game was played")
    )

    table = models.ForeignKey(Table, blank=True, null=True, related_name="games", verbose_name=_("table"))

    class Meta:
        ordering = ['-played_at']

    def __str__(self):
        return " - ".join(map(str, self.teams.all()))


class Team(models.Model):
    UNKNOWN = 0
    RED = 1
    BLUE = 2
    SIDE_CHOICES = (
        (UNKNOWN, _("Unknown")),
        (RED, _("Red")),
        (BLUE, _("Blue")),
    )
    side = models.IntegerField(db_index=True, choices=SIDE_CHOICES, default=UNKNOWN, verbose_name=_("side"))

    game = models.ForeignKey(Game, related_name="teams", on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(
        verbose_name=_("score"),
        help_text=_("Team's score in the game"),
        validators=[MaxValueValidator(limit_value=10)]
    )
    players = models.ManyToManyField(User)

    def __str__(self):
        return "%s (%s)" % (
            self.score,
            ", ".join(map(str, self.players.all()))
        )


class Player(models.Model):
    user = models.OneToOneField(User)
    singles_wins = models.PositiveIntegerField(
        verbose_name=_("wins - singles"),
        help_text=_("Wins in a single player team"),
        default=0
    )
    singles_win_percentage = models.DecimalField(
        verbose_name=_("win percentage - singles"),
        help_text=_("Win percentage for single player team games"),
        default=0,
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(limit_value=0), MaxValueValidator(limit_value=100)]
    )
    doubles_wins = models.PositiveIntegerField(
        verbose_name=_("wins - doubles"),
        help_text=_("Wins in a two player team"),
        default=0
    )
    doubles_win_percentage = models.DecimalField(
        verbose_name=_("win percentage - doubles"),
        help_text=_("Win percentage in two player team games"),
        default=0,
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(limit_value=0), MaxValueValidator(limit_value=100)]
    )
    total_played = models.PositiveIntegerField(
        verbose_name=_("total played"),
        help_text=_("Total games played in"),
        default=0
    )
    singles_played = models.PositiveIntegerField(
        verbose_name=_("singles played"),
        help_text=_("Total games played as a single player team"),
        default=0
    )
    doubles_played = models.PositiveIntegerField(
        verbose_name=_("doubles played"),
        help_text=_("Total games played in a two player team"),
        default=0
    )
    colour = models.CharField(
        verbose_name=_("colour code"),
        help_text=_("Player colour as a hex colour code"),
        max_length=7, null=True
    )

    def __str__(self):
        return "Player %s" % self.user.name if self.user.name else self.user.username

    def save(self, *args, **kwargs):
        """
        Init some data for the player.
        """
        if not self.pk or not self.colour:
            self.colour = random_colour()
        return super(Player, self).save(*args, **kwargs)
