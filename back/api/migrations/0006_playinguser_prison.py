# Generated by Django 3.0.4 on 2020-06-07 09:40

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_transaction_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='playinguser',
            name='prison',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Więzienie'),
        ),
    ]
