# Generated by Django 3.0.4 on 2020-05-09 15:20

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nazwa akcji')),
            ],
            options={
                'verbose_name': 'Akcje',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nazwa pola')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='Cena za pole')),
            ],
            options={
                'verbose_name': 'Pole',
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255, verbose_name='Nazwa typu pola')),
                ('parameter', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='Parametry typu pola')),
            ],
            options={
                'verbose_name': 'Wiadomośći',
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nazwa dzielnicy')),
                ('price_per_house', models.IntegerField(verbose_name='Cena za domek')),
            ],
            options={
                'verbose_name': 'Strefa',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='Cena za pole')),
                ('isBuyingOffer', models.BooleanField(verbose_name='Oferta kupna')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_buyer', to=settings.AUTH_USER_MODEL, verbose_name='Kupujący')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='api.Field', verbose_name='Pole')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_seller', to=settings.AUTH_USER_MODEL, verbose_name='Sprzedający')),
            ],
            options={
                'verbose_name': 'Oferty',
            },
        ),
        migrations.CreateModel(
            name='PlayingUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.IntegerField(blank=True, null=True, verbose_name='Kolejność')),
                ('isActive', models.BooleanField(default=False, verbose_name='Aktywyny ruch')),
                ('isPlaying', models.BooleanField(default=False, verbose_name='Grający')),
                ('budget', models.IntegerField(blank=True, null=True, verbose_name='Budżet')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playing_users', to='api.Field', verbose_name='Pole')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playing_users', to=settings.AUTH_USER_MODEL, verbose_name='Sprzedający')),
            ],
            options={
                'verbose_name': 'Grający użytkownicy',
            },
        ),
        migrations.CreateModel(
            name='FieldType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nazwa typu pola')),
                ('parameter', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Parametry typu pola')),
                ('action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='field_types', to='api.Action', verbose_name='Akcja')),
            ],
            options={
                'verbose_name': 'Typ pola',
            },
        ),
        migrations.AddField(
            model_name='field',
            name='field_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='api.FieldType', verbose_name='Typ pola'),
        ),
        migrations.AddField(
            model_name='field',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='api.Zone', verbose_name='Dzielnica'),
        ),
        migrations.CreateModel(
            name='Estate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_zero_houses', models.IntegerField(verbose_name='Czynsz za zero posiadłości')),
                ('fee_one_house', models.IntegerField(verbose_name='Czynsz za jedną posiadłość')),
                ('fee_two_houses', models.IntegerField(verbose_name='Czynsz za dwie posiadłości')),
                ('fee_three_houses', models.IntegerField(verbose_name='Czynsz za trzy posiadłości')),
                ('fee_four_houses', models.IntegerField(verbose_name='Czynsz za cztery posiadłości')),
                ('fee_five_houses', models.IntegerField(verbose_name='Czynsz za pięć posiadłości')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estates', to='api.Field', verbose_name='Pole')),
            ],
            options={
                'verbose_name': 'Posiadłości',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Opis karty')),
                ('parameter', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='Parametry karty')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='api.Action', verbose_name='Akcja')),
            ],
            options={
                'verbose_name': 'Karta',
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estateNumber', models.IntegerField(blank=True, null=True, verbose_name='Liczba domków')),
                ('isPledged', models.BooleanField(default=False, verbose_name='Zastawiona nieruchomość')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='api.Field', verbose_name='Pole')),
                ('playingUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='api.PlayingUser', verbose_name='Uzytkownik')),
            ],
            options={
                'verbose_name': 'Posiadłości',
            },
        ),
    ]
