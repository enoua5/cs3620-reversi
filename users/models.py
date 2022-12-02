from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    elo_rating = models.IntegerField(default=1000)
    open_for_challenge = models.BooleanField(default=True)
    bio_text = models.CharField(max_length=2000, default="Hi! I'm new here!")


