from django.contrib.auth.models import User
from django.db import models


class Contribution(models.Model):
    member = models.ForeignKey(User)
    amount = models.IntegerField(default=0)
    date_paid = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    date_approved = models.DateTimeField(null=True)


class ConfirmationRequest(models.Model):
    contribution = models.ForeignKey(Contribution)
    approved = models.BooleanField(default=False)
    date_requested = models.DateTimeField(auto_now_add=True)
