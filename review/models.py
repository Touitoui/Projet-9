from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Review(models.Model):
    ticket = models.ForeignKey(to="ticket.Ticket", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)