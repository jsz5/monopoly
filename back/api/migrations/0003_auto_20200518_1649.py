# Generated by Django 3.0.4 on 2020-05-18 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200512_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='estateNumber',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Liczba domków'),
        ),
    ]
