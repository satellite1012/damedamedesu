from django.db import models
from django.contrib.auth.models import User
        
class Song(models.Model):
    recommender = models.ForeignKey(
        User,
        related_name='+',
    )
    suggested_members = models.ManyToManyField(User)
    name = models.CharField(max_length=128)
    url = models.URLField()
    time_added = models.DateTimeField(auto_now_add=True)
    
    srank = models.PositiveIntegerField(null=True, blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True)
    comment = models.CharField(max_length=2048, null=True, blank=True)
    turn_time = models.DateTimeField(null=True, blank=True)
    
class Turn(models.Model):
    owner = models.ForeignKey(User)
    song_list = models.ManyToManyField(Song)
    
class Group(models.Model):
    member_list = models.ManyToManyField(User)
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    turn = models.IntegerField()
    prev_turn = models.ForeignKey(Turn, null=True, blank=True)
    