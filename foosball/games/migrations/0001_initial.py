# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-08 08:15
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('played_at', models.DateTimeField(default=datetime.datetime.now, help_text='Time when the game was played', verbose_name='played at')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games_created', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('modified_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games_modified', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
            ],
            options={
                'ordering': ['-played_at'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('side', models.IntegerField(choices=[(0, 'Unknown'), (1, 'Red'), (2, 'Blue')], db_index=True, default=0, verbose_name='side')),
                ('score', models.PositiveSmallIntegerField(help_text="Team's score in the game", validators=[django.core.validators.MaxValueValidator(limit_value=10)], verbose_name='score')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='games.Game')),
                ('players', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]