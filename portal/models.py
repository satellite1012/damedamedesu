from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    day = models.DateField()
    win = models.IntegerField()
    champs = models.CharField(max_length=2048) #encoded as name1/name2/name3/name4/name5
    
