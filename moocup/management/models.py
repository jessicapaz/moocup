import uuid

from django.db import models
from django.utils import timezone

from ..users.models import User
from ..users.models import Product


class UseManagement(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    timestamp = models.DateTimeField(
        default=timezone.now
    )


class Dashboard(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT
    )
    accumulated_points = models.IntegerField()
    saved_cups = models.IntegerField()
    consumed_water = models.FloatField()


class Voucher(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT
    )
    points = models.IntegerField()
