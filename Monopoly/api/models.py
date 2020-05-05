from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField


class Estate(models.Model):
    fee_zero_houses = models.IntegerField(verbose_name=_("Czynsz za zero posiadłości"))
    fee_one_house = models.IntegerField(verbose_name=_("Czynsz za jedną posiadłość"))
    fee_two_houses = models.IntegerField(verbose_name=_("Czynsz za dwie posiadłości"))
    fee_three_houses = models.IntegerField(verbose_name=_("Czynsz za trzy posiadłości"))
    fee_four_houses = models.IntegerField(verbose_name=_("Czynsz za cztery posiadłości"))
    fee_five_houses = models.IntegerField(verbose_name=_("Czynsz za pięć posiadłości"))
    fee_six_houses = models.IntegerField(verbose_name=_("Czynsz za sześć posiadłości"))


class Zone(models.Model):
    name = models.CharField(verbose_name=_("Nazwa dzielnicy"), max_length=255)
    price_per_house = models.IntegerField(verbose_name=_("Cena za domek"))


class Action(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Nazwa akcji"))


class FieldType(models.Model):
    name = models.CharField(verbose_name=_("Nazwa typu pola"), max_length=255)
    parameter = JSONField(verbose_name=_("Parametry typu pola"))
    action = models.ForeignKey(
        Action, related_name="field_types", on_delete=models.CASCADE, verbose_name=_("Akcja")
    )


class Card(models.Model):
    description = models.TextField(verbose_name=_("Opis karty"))
    parameter = JSONField(verbose_name=_("Parametry karty"))
    action = models.ForeignKey(
        Action, related_name="cards", on_delete=models.CASCADE, verbose_name=_("Akcja")
    )


class Field(models.Model):
    price = models.IntegerField(verbose_name=_("Cena za pole"), null=True, blank=True)
    field_type = models.ForeignKey(
        FieldType, related_name="fields", on_delete=models.CASCADE, verbose_name=_("Typ pola")
    )
    zone = models.ForeignKey(
        Zone, related_name="fields", on_delete=models.CASCADE, verbose_name=_("Dzielnica")
    )
    estate = models.OneToOneField(Estate, on_delete=models.CASCADE, related_name="estate")
