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

