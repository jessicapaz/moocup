# Generated by Django 2.1.7 on 2019-04-28 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0005_auto_20190428_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='user',
            field=models.OneToOneField(default='6c13c93f-c105-48a4-a785-54c466d4a74e', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
