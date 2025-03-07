from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    tickets = models.ManyToManyField("ticket.Ticket", related_name='users')
    user_follows = models.ManyToManyField("user_follows.UserFollows", related_name='users')
    reviews = models.ManyToManyField("review.Review", related_name='users')
