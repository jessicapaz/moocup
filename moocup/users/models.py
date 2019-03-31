import uuid
from datetime import datetime

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token

from .managers import UserManager


@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        db_index=True,
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
    )
    product_code = models.ForeignKey(
        'Product',
        on_delete=models.PROTECT,
        unique=True,
        null=True,
        blank=True
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Acessa Painel Admin",
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    description = models.CharField(
        max_length=100,
        default="Garrafa",
    )
    timestamp = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f'{self.id}'
