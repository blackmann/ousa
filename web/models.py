from django.contrib.auth.models import User
from django.db import models


class Contribution(models.Model):
    member = models.ForeignKey(User)
    amount = models.IntegerField(default=0)
    date_paid = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    date_approved = models.DateTimeField(null=True)

    class Meta:
        ordering = ("-date_paid",)


class ConfirmationRequest(models.Model):
    contribution = models.OneToOneField(Contribution)
    approved = models.BooleanField(default=False)
    date_requested = models.DateTimeField(auto_now_add=True)
    merchant = models.CharField(blank=True, max_length=255)
    reference = models.CharField(blank=True, max_length=100)


class Admin(models.Model):
    member = models.ForeignKey(User)
    is_admin = models.BooleanField(default=False)
