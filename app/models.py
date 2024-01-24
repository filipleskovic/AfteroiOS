from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    date_of_birth = models.DateTimeField
    gender = models.CharField(max_lenght=32)
    avatar_url = models.CharField(max_lenght=128)


class PartyPosters(models.Model):
    party_url = models.CharField(max_lenght=128)


class Party(models.Model):
    title = models.CharField(max_lenght=128)
    total_allowed_guest = models.SmallIntegerField
    description = models.CharField(max_lenght=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField()
    location = models.CharField(max_lenght=128)
    party_poster_fk = models.ForeignKey(PartyPosters, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Recension(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_lenght=512)
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )


class PartyGuest(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
