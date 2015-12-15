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
    
class Turn(models.Model):
    owner = models.ForeignKey(Member)
    song_list = models.ManyToManyField(
        Song,
        through='Evaluation',
        through_fields=('turn', 'song'),
    )
    turn_time = models.DateTimeField(auto_now_add=True)
    
class Group(models.Model):
    member_list = models.ManyToManyField(Member)
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    turn = models.IntegerField()
    history = models.ManyToManyField(Turn)
    
class Evaluation(models.Model):
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()
    rating = models.PositiveIntegerField()
    comment = models.CharField(max_length=1024)
    
    