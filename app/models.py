from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    date_of_birth = models.DateTimeField
    gender = models.CharField(max_length=32)
    avatar_url = models.CharField(max_length=128)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='afterios_group',  
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='afterios_permissions', 
        help_text='Specific permissions for this user.',
    )


class PartyPosters(models.Model):
    party_url = models.CharField(max_length=128)


class Party(models.Model):
    title = models.CharField(max_length=128)
    total_allowed_guest = models.SmallIntegerField
    description = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField()
    location = models.CharField(max_length=128)
    party_poster_fk = models.ForeignKey(PartyPosters, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Recension(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )


class PartyGuest(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
