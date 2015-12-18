from django.db import models
from django.contrib.auth.models import User
    
class Member(models.Model):
    user = models.OneToOneField(User)
        
class Song(models.Model):
    recommender = models.ForeignKey(
        Member,
        related_name='+',
    )
    suggested_members = models.ManyToManyField(Member)
    name = models.CharField(max_length=128)
    url = models.URLField()
    time_added = models.DateTimeField(auto_now_add=True)
    
    rank = models.PositiveIntegerField()
    rating = models.PositiveIntegerField()
    comment = models.CharField(max_length=2048)
    turn_time = models.DateTimeField()
    
class Turn(models.Model):
    owner = models.ForeignKey(Member)
    song_list = models.ManyToManyField(Song)
    
class Group(models.Model):
    member_list = models.ManyToManyField(Member)
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    turn = models.IntegerField()
    prev_turn = models.ForeignKey(Turn)    
    