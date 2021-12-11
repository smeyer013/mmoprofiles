from django.db import models
from django.contrib.auth import get_user_model


# A game, with its name and description.
# Used in GameInstance objects.
class Game(models.Model):
    name = models.CharField(max_length=128)
    players = models.IntegerField(default=0)
    def __str__(self):
        return self.name

# An instance of a game, used for user profiles.
# Having a game registered on a user's profile
# allows them to set up guilds and specs for it.
class GameInstance(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    level = models.CharField(max_length=10,default="")
    active = models.BooleanField(default=True)

# An instance of a spec, used for user profiles.
# Specs are basically the user's role in gameplay,
# plus the class or build they use to do that.
class SpecInstance(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    role = models.CharField(max_length=32,default="")
    spec = models.CharField(max_length=32,default="")

# An instance of a guild, used for user profiles.
# Guilds are groups of players that play the same game.
class GuildInstance(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    guild_name = models.CharField(max_length=64,default="")

