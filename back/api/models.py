from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User


# class Game(models.Model):
#     name = models.CharField(verbose_name=_("Nazwa gry"), max_length=255)
#
#     completed = models.DateTimeField(null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#
#     # players with info about
#
#     @staticmethod
#     def get_by_id(id):
#         try:
#             return Game.objects.get(pk=id)
#         except Game.DoesNotExist:
#             # TODO: Handle this Exception
#             pass
#
#     @staticmethod
#     def create_new(name):
#         """
#         Create a new game and game squares
#         :param user: the user that created the game
#         :return: a new game object
#         """
#         # make the game's name from the name of game
#         # TODO: Everything, user ect.
#         new_game = Game(name=name)
#         new_game.save()
#
#         return new_game


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
    parameter = JSONField(verbose_name=_("Parametry karty"),null=True, blank=True)
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
    fee_zero_houses = models.IntegerField(verbose_name=_("Czynsz za zero posiad??o??ci"))
    fee_one_house = models.IntegerField(verbose_name=_("Czynsz za jedn?? posiad??o????"))
    fee_two_houses = models.IntegerField(verbose_name=_("Czynsz za dwie posiad??o??ci"))
    fee_three_houses = models.IntegerField(verbose_name=_("Czynsz za trzy posiad??o??ci"))
    fee_four_houses = models.IntegerField(
        verbose_name=_("Czynsz za cztery posiad??o??ci")
    )
    fee_five_houses = models.IntegerField(verbose_name=_("Czynsz za pi???? posiad??o??ci"))

    class Meta:
        verbose_name = _("Posiad??o??ci")


class Transaction(models.Model):
    seller = models.ForeignKey(
        User,
        related_name="transactions_seller",
        on_delete=models.CASCADE,
        verbose_name=_("Sprzedaj??cy"),
    )
    buyer = models.ForeignKey(
        User,
        related_name="transactions_buyer",
        on_delete=models.CASCADE,
        verbose_name=_("Kupuj??cy"),
    )
    field = models.ForeignKey(
        Field,
        related_name="transactions",
        on_delete=models.CASCADE,
        verbose_name=_("Pole"),
    )
    price = models.IntegerField(verbose_name=_("Cena za pole"), null=True, blank=True)
    isBuyingOffer = models.BooleanField(verbose_name=_("Oferta kupna"))
    finished = models.BooleanField(verbose_name=_("Oferta zako??czona"), default=False)

    class Meta:
        verbose_name = _("Oferty")


class PlayingUser(models.Model):
    user = models.ForeignKey(
        User,
        related_name="playing_users",
        on_delete=models.CASCADE,
        verbose_name=_("Sprzedaj??cy"),
        unique=True
    )
    place = models.IntegerField(verbose_name=_("Kolejno????"), null=True, blank=True)
    isActive = models.BooleanField(verbose_name=_("Aktywyny ruch"), default=False)
    isPlaying = models.BooleanField(verbose_name=_("Graj??cy"), default=False)
    budget = models.IntegerField(verbose_name=_("Bud??et"), null=True, blank=True)
    field = models.ForeignKey(
        Field,
        related_name="playing_users",
        on_delete=models.CASCADE,
        verbose_name=_("Pole"),
        null=True,
        blank=True,
    )
    dice = models.BooleanField(verbose_name=_("Rzut kostk??"), default=False)
    prison = models.IntegerField(verbose_name=_("Liczba kolejek w wi??zieniu"), null=True, blank=True)
    get_out_of_jail_card = models.IntegerField(verbose_name=_("Karta wyjd?? z wi??zienia"), default=0)

    class Meta:
        verbose_name = _("Graj??cy u??ytkownicy")


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
        verbose_name=_("Liczba domk??w"), null=True, blank=True, default=0
    )
    isPledged = models.BooleanField(
        verbose_name=_("Zastawiona nieruchomo????"), default=False
    )

    class Meta:
        verbose_name = _("Posiad??o??ci")


class Messages(models.Model):
    type = models.CharField(verbose_name=_("Nazwa typu pola"), max_length=255)
    parameter = JSONField(verbose_name=_("Parametry typu pola"))

    class Meta:
        verbose_name = _("Wiadomo????i")
