# Generated by Django 3.0.4 on 2020-06-02 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200527_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='finished',
            field=models.BooleanField(default=False, verbose_name='Oferta zakończona'),
        ),
    ]
