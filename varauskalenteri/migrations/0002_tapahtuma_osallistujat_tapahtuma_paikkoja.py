# Generated by Django 4.1.1 on 2022-09-20 06:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('varauskalenteri', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tapahtuma',
            name='osallistujat',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tapahtuma',
            name='paikkoja',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
