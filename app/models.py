from datetime import timedelta, datetime
from django.utils import timezone
from email.policy import default
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    date_of_birth = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=32)
    avatar_url = models.CharField(max_length=128)
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        related_name="afterios_group",
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        related_name="afterios_permissions",
        help_text="Specific permissions for this user.",
    )
    
    def get_previous_parties(self):
        current_datetime = datetime.now()
        previous_parties = Party.objects.filter(created_by=self, closed_at__lt=current_datetime)
        return previous_parties

    def get_current_parties(self):
        current_datetime = datetime.now()
        previous_parties = Party.objects.filter(created_by=self, closed_at__gt=current_datetime)
        return previous_parties
    
    def get_attended_parties(self):
        current_datetime = datetime.now()
        attended_parties = Party.objects.filter(
            closed_at__lt=current_datetime,
            partyguest__user_id=self
        ).distinct()
        return attended_parties

class PartyPosters(models.Model):
    party_url = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f"poster num {self.id}"


class Party(models.Model):
    title = models.CharField(max_length=128)
    total_allowed_guest = models.SmallIntegerField(default=10)
    description = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    starts_at = models.DateTimeField()
    closed_at = models.DateTimeField()
    location = models.CharField(max_length=128)
    party_poster_fk = models.ForeignKey(PartyPosters, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_finished(self):
        return timezone.now() + timedelta(hours=1) > self.closed_at

    def __str__(self) -> str:
        return f"{self.title}"


class Recension(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self) -> str:
        return f"{self.user_id.username} recension for {self.party_id.title}"


class PartyGuest(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"user: {self.user_id.username} party: {self.party_id.title}"


class PartyRequest(models.Model):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DECLINED = "DECLINED"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (DECLINED, "Declined"),
    ]

    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    text = models.CharField(max_length=1024, default="Prazno")

    def __str__(self):
        return f"{self.user_id.username}'s request for {self.party_id} - {self.status}"
