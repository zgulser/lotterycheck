from django.db import models
from django_unixdatetimefield import UnixDateTimeField
import uuid

# Create your models here.

class Lottery(models.Model):
    created_at = UnixDateTimeField(auto_now=True)
    token = models.UUIDField(primary_key=True, default=uuid.uuid4)
    duration = models.IntegerField(default=30)
    expired = models.BooleanField(default=False)
    winner_row = models.IntegerField(default=-1)

# a model to represent form data assuming form includes the following fields
class LotteryPlayer(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    identity = models.IntegerField(primary_key=True)
    token = models.UUIDField(default=uuid.uuid4)
