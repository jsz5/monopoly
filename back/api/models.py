from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User


class Zone(models.Model):
    name = models.CharField(verbose_name=_("Nazwa dzielnicy"), max_length=255)
    price_per_house = models.IntegerField(verbose_name=_("Cena za domek"))

    class Meta:
        verbose_name = _("Strefa")


class Action(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Nazwa akcji"))

    class Meta:
        verbose_name = _("Akcje")


class FieldType(models.Model):
    name = models.CharField(verbose_name=_("Nazwa typu pola"), max_length=255)
    parameter = JSONField(verbose_name=_("Parametry typu pola"), null=True, blank=True)
    action = models.ForeignKey(
        Action,
        related_name="field_types",
        on_delete=models.CASCADE,
        verbose_name=_("Akcja"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Typ pola")

    @property
    def get_field(self):
        return self.fields.filter(field_type=self).first()


class Card(models.Model):
    description = models.TextField(verbose_name=_("Opis karty"))
    parameter = JSONField(verbose_name=_("Parametry karty"))
    action = models.ForeignKey(
        Action, related_name="cards", on_delete=models.CASCADE, verbose_name=_("Akcja")
    )

    class Meta:
        verbose_name = _("Karta")


class Field(models.Model):
    name = models.CharField(
        verbose_name=_("Nazwa pola"), max_length=255, null=True, blank=True
    )
    price = models.IntegerField(verbose_name=_("Cena za pole"), null=True, blank=True)
    field_type = models.ForeignKey(
        FieldType,
        related_name="fields",
        on_delete=models.CASCADE,
        verbose_name=_("Typ pola"),
    )
    zone = models.ForeignKey(
        Zone,
        related_name="fields",
        on_delete=models.CASCADE,
        verbose_name=_("Dzielnica"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Pole")


class Estate(models.Model):
    field = models.ForeignKey(
        Field, related_name="estates", on_delete=models.CASCADE, verbose_name=_("Pole"),
    )
    fee_zero_houses = models.IntegerField(verbose_name=_("Czynsz za zero posiadłości"))
    fee_one_house = models.IntegerField(verbose_name=_("Czynsz za jedną posiadłość"))
    fee_two_houses = models.IntegerField(verbose_name=_("Czynsz za dwie posiadłości"))
    fee_three_houses = models.IntegerField(verbose_name=_("Czynsz za trzy posiadłości"))
    fee_four_houses = models.IntegerField(
        verbose_name=_("Czynsz za cztery posiadłości")
    )
    fee_five_houses = models.IntegerField(verbose_name=_("Czynsz za pięć posiadłości"))

    class Meta:
        verbose_name = _("Posiadłości")


class Transaction(models.Model):
    seller = models.ForeignKey(
        User,
        related_name="transactions_seller",
        on_delete=models.CASCADE,
        verbose_name=_("Sprzedający"),
    )
    buyer = models.ForeignKey(
        User,
        related_name="transactions_buyer",
        on_delete=models.CASCADE,
        verbose_name=_("Kupujący"),
    )
    field = models.ForeignKey(
        Field,
        related_name="transactions",
        on_delete=models.CASCADE,
        verbose_name=_("Pole"),
    )
    price = models.IntegerField(verbose_name=_("Cena za pole"), null=True, blank=True)
    isBuyingOffer = models.BooleanField(verbose_name=_("Oferta kupna"))

    class Meta:
        verbose_name = _("Oferty")


class PlayingUser(models.Model):
    user = models.ForeignKey(
        User,
        related_name="playing_users",
        on_delete=models.CASCADE,
        verbose_name=_("Sprzedający"),
    )
    place = models.IntegerField(verbose_name=_("Kolejność"), null=True, blank=True)
    isActive = models.BooleanField(verbose_name=_("Aktywyny ruch"), default=False)
    isPlaying = models.BooleanField(verbose_name=_("Grający"), default=False)
    budget = models.IntegerField(verbose_name=_("Budżet"), null=True, blank=True)
    field = models.ForeignKey(
        Field,
        related_name="playing_users",
        on_delete=models.CASCADE,
        verbose_name=_("Pole"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Grający użytkownicy")


class Asset(models.Model):
    playingUser = models.ForeignKey(
        PlayingUser,
        related_name="assets",
        on_delete=models.CASCADE,
        verbose_name=_("Uzytkownik"),
    )
    field = models.ForeignKey(
        Field, related_name="assets", on_delete=models.CASCADE, verbose_name=_("Pole")
    )
    estateNumber = models.IntegerField(
        verbose_name=_("Liczba domków"), null=True, blank=True, default=0
    )
    isPledged = models.BooleanField(
        verbose_name=_("Zastawiona nieruchomość"), default=False
    )

    class Meta:
        verbose_name = _("Posiadłości")


class Messages(models.Model):
    type = models.CharField(verbose_name=_("Nazwa typu pola"), max_length=255)
    parameter = JSONField(verbose_name=_("Parametry typu pola"))

    class Meta:
        verbose_name = _("Wiadomośći")
