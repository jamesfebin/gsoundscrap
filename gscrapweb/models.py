from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
	pass

class Track(models.Model):
	author = models.TextField()
	author_link = models.TextField()
	track_type = models.TextField()
	user_id = models.IntegerField()
	title = models.TextField()
	link = models.TextField()
	thumbnail = models.TextField()
	embed = models.TextField(default='')
