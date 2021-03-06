import json

from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
    ListCreateAPIView,
)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib import auth
from rest_framework.authtoken.models import Token
from api.models import PlayingUser, FieldType, Field, Messages, Asset, Estate, Card
from rest_auth.serializers import LoginSerializer
from rest_auth.views import LogoutView
import random

from django.http import HttpResponse
from django.db.models import Q
from django.http import Http404

from api.serializers import (
    PlayingUserSerializer,
    EstateSerializer,
    FieldSerializer,
    FieldEstateSerializer,
    CardSerializer,
    AssetSerializer
)

from django.views.generic import CreateView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from api.models import Transaction
from api.serializers import TransactionListSerializer, CreateTransactionSerializer
from django.contrib.auth.models import User


class PlayingUserReadyUpdateView(APIView):
    queryset = PlayingUser.objects.all()
    serializer_class = None

    def put(self, request, format=None):
        user = PlayingUser.objects.get(user=request.user)
        user.isActive = True
        user.save()
        all_users = PlayingUser.objects.count()
        active_users = PlayingUser.objects.filter(isActive=True).count()
        if active_users == 4 or active_users == all_users:
            playing_order = list(PlayingUser.objects.filter(isActive=True))
            random.shuffle(playing_order)
            start_field = FieldType.objects.filter(name="START").first().get_field
            for place, playing_user in enumerate(playing_order):
                if place == 0:
                    playing_user.isPlaying = True
                playing_user.place = place + 1
                playing_user.field = start_field
                playing_user.budget = 15000
                playing_user.save()
            return Response({"show_board": True, "message": "Gra rozpocz??ta."})

        return Response({"show_board": False, "message": "Gracz jest gotowy do gry."})


class Login(CreateAPIView):
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        validated_data = self.serializer_class(request.data).data
        username = validated_data["username"]
        password = validated_data["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                start_game_button = self.__add_playing_user(user)
                number_of_users = PlayingUser.objects.count()
                return Response(
                    {
                        "key": token.key,
                        "start_game_button": start_game_button,
                        "number_of_users": number_of_users,
                    }
                )
        return Response("Invalid username or password", status=401)

    def __add_playing_user(self, user):
        if PlayingUser.objects.filter(user=user).count() == 0:
            PlayingUser(user=user).save()
        if not PlayingUser.objects.filter(isPlaying=True).first():
            if PlayingUser.objects.all().count() >= 2:
                return True  # gracze z tabeli mog?? rozpocz???? gr?? (przycisk ROZPOCZNIJ GR?? jest dost??pny) - event
        return False


class Logout(LogoutView):
    def post(self, request, *args, **kwargs):
        user = request.user
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            PlayingUser.objects.filter(user_id=user.id).delete()
        return response


class PlayingUserListView(ListAPIView):
    serializer_class = PlayingUserSerializer
    queryset = PlayingUser.objects.all()


class AuthUserView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            auth_playing = PlayingUser.objects.get(user=request.user)
            current_playing_id = PlayingUser.objects.get(isPlaying=True).user_id
            return Response(
                {
                    "username": request.user.username,
                    "budget": auth_playing.budget,
                    "field": auth_playing.field_id,
                    "turn": auth_playing.isPlaying,
                    "turn_user": User.objects.get(id=current_playing_id).username
                }
            )
        except Exception:
            return Response("Wyst??pi?? b????d", status=500)


class UserBudgetView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            playing_user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawid??owy u??ytkownik", status=403)
        if playing_user.isActive:
            return Response({"budget": playing_user.budget})
        else:
            return Response("Podany u??ytkownik nie jest aktywny", status=406)


class UserFieldView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            playing_user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawid??owy u??ytkownik", status=403)
        if playing_user.isActive:
            return Response({"field": playing_user.field})
        else:
            return Response("Podany u??ytkownik nie jest aktywny", status=406)


class PlayingUserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlayingUserSerializer

    def get(self, request, *args, **kwargs):
        playing_user = PlayingUser.objects.get(user=request.user)
        return Response(PlayingUserSerializer(playing_user).data)


class CurrentPlayerView(APIView):
    def get(self, request, *args, **kwargs):
        current_playing_id = PlayingUser.objects.get(isPlaying=True).user_id
        auth_playing = PlayingUser.objects.get(user=request.user)
        return Response(
            {
                "turn": auth_playing.isPlaying,
                "turn_user": User.objects.get(id=current_playing_id).username
            }
        )


class DiceRollView(ListAPIView):
    """
    Active and playing user dice roll, function modify standing field
    """

    def get(self, request, *args, **kwargs):
        self.error = None
        self.dice = random.randint(1, 12)
        self.response = {"number": self.dice}
        try:
            self.user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawid??owy u??ytkownik", status=403)
        if  self.user.dice:
            return Response("U??ytkownik nie ma prawa ruchu", status=403)

        if self.user.isActive and self.user.isPlaying:
            if self.user.prison:
                self.user.prison -= 1
                self.user.dice=True
                self.user.save()
                return Response(f"Jeste?? w wi??zieniu. Zosta??o kolejek { self.user.prison}")
            field_count = Field.objects.all().count()
            if int(self.user.field.pk) + self.dice > field_count:
                self.user.budget += 2000
                self.field = Field.objects.get(pk=int(self.user.field.pk + self.dice - field_count))
            else:
                self.field = Field.objects.get(pk=int(self.user.field.pk + self.dice))
            try:
                self.asset = Asset.objects.get(field=self.field)
                if self.asset.isPledged:
                    self.asset = None
            except Asset.DoesNotExist:
                self.asset = None

            self.response.update(self.check_field_type())
            if self.error is not None:
                return Response(self.error, status=403)

            if self.user.budget < 0:
                for asset in Asset.objects.filter(playingUser=self.user):
                    self.user.budget += asset.price + asset.estateNumber * asset.field.zone.price_per_house
                    asset.delete()
                    if self.user.budget > 0:
                        break

            if self.user.budget < 0:
                self.user.isActive = False
                return Response("Przegrana gra")

            self.user.field = self.field
            self.user.dice = True
            self.user.save()

            return Response(self.response)
        else:
            return Response("U??ytkownik nie ma prawa ruchu", status=403)

    def check_field_type(self):
        response = dict()
        response['name'] = self.field.name
        print(self.field.field_type)
        if self.field.field_type_id == 2:
            response['action'] = 'visit jail'
        elif self.field.field_type_id == 3:
            card_id = random.randint(1, Card.objects.count())
            response['action'] = 'get_card'
            response['card'] = self.card(card_id)

        elif self.field.field_type_id == 4:
            to_pay = 2000 if self.field.pk == 39 else 1000
            self.user.budget -= to_pay
            response['action'] = 'pay tax'
            response['amount'] = to_pay
        elif self.field.field_type_id == 5:
            self.user.prison = 2
            self.move(11)
            self.user.save()
            response['action'] = 'go to jail'
        elif self.field.field_type_id == 7:
            # normal
            response['action'] = 'normal card'
            if self.asset:
                if self.asset.playingUser != self.user:
                    estate = Estate.objects.get(field=self.field)
                    if self.asset.estateNumber == 0:
                        fee = estate.fee_zero_houses
                    elif self.asset.estateNumber == 1:
                        fee = estate.fee_one_house
                    elif self.asset.estateNumber == 2:
                        fee = estate.fee_two_houses
                    elif self.asset.estateNumber == 3:
                        fee = estate.fee_three_houses
                    elif self.asset.estateNumber == 4:
                        fee = estate.fee_four_houses
                    elif self.asset.estateNumber == 5:
                        fee = estate.fee_five_houses
                    response['pay'] = fee
                    response['to_who'] = self.asset.playingUser.user.username
                    self.user.budget -= fee
                else:
                    response['my'] = True
            else:
                response['price'] = self.field.price
        elif self.field.field_type_id == 8:
            # power plant
            response['action'] = 'power_plant'
            if self.asset:
                if self.asset.playingUser != self.user:
                    # if player has one power plant
                    power_plants_number = Asset.objects.filter(
                        Q(field__in=Field.objects.filter(field_type=8)),
                        Q(playingUser_id=self.asset.playingUser)
                    ).count()
                    fee = self.dice * 400 if power_plants_number == 1 else self.dice * 1000
                    self.user.budget -= fee
                    response['pay'] = fee
                    response['to_who'] = self.asset.playingUser.user.username
                else:
                    response['my'] = True
            else:
                response['price'] = self.field.price
        elif self.field.field_type_id == 9:
            response['action'] = 'transport'
            if self.asset:
                if self.asset.playingUser != self.user:
                    transport_number = Asset.objects.filter(
                        Q(field__in=Field.objects.filter(field_type=9)),
                        Q(playingUser_id=self.asset.playingUser)
                    ).count()
                    if transport_number == 1:
                        fee = 250
                    elif transport_number == 2:
                        fee = 500
                    elif transport_number == 3:
                        fee = 1000
                    elif transport_number == 4:
                        fee = 2000
                    self.user.budget -= fee
                    response['pay'] = fee
                    response['to_who'] = self.asset.playingUser.user.username
                else:
                    response['my'] = True
            else:
                response['price'] = self.field.price

        return dict(response)

    def card(self, card_id):
        print("Card")
        print(card_id)
        try:
            card = Card.objects.get(pk=card_id)
            print(card)
        except Card.DoesNotExist:
            self.error = "Card does't exist"
        self.card_data = CardSerializer(card).data

        self.parameter = self.card_data["parameter"]
        print(self.card_data["action_id"])
        if self.card_data["action_id"] == 1:
            # MOVE
            self.__move()
        elif self.card_data["action_id"] == 2:
            # MOVE TO
            self.__move_to()
        elif self.card_data["action_id"] == 4:
            # PAY ALL USERS
            self.__pay_all_users()
        elif self.card_data["action_id"] == 5:
            # PAY BANK
            self.user.budget -= self.parameter["pay"]
        elif self.card_data["action_id"] == 6:
            # GET OUT OF JAIL CARD
            self.user.get_out_of_jail_card += 1
        elif self.card_data["action_id"] == 7:
            # PAY_FOR_ASSETS
            self.__pay_for_assets()
        elif self.card_data["action_id"] == 8:
            # GET_MONEY_FROM_USERS
            self.__get_money_from_users()
        elif self.card_data["action_id"] == 9:
            # GET_MONEY_FROM_BANK
            self.user.budget += self.parameter["get"]
        elif self.card_data["action_id"] == 10:
            # GO TO JAIL
            self.user.prison = {"queue": 2, "checked": True}
            self.move(11)

        return dict(self.card_data)

    def move(self, field_id):
        self.user.field_id = field_id
        self.field = Field.objects.get(pk=field_id)

    def __move(self):
        new_field_id = (self.field.pk + self.parameter["number"])
        field_count = Field.objects.all().count()
        if int(new_field_id) > field_count:
            new_field_id = int(new_field_id) % field_count
        elif int(new_field_id) <= 0:
            new_field_id = new_field_id + field_count
        self.move(new_field_id)

        self.card_data["new_field_id"] = new_field_id
        self.card_data['move'] = self.check_field_type()

    def __move_to(self):
        if 'dice' in self.parameter:
            self.dice = random.randint(1, 12)
            self.card_data['new_dice'] = self.dice
        if 'field_type' in self.parameter:
            new_field = Field.objects.filter(
                Q(field_type_id=self.parameter['field_type']),
                Q(id__gt=self.field.id)
            ).order_by('id').first()
            self.move(new_field.pk)

            self.card_data['move'] = self.check_field_type()
        elif 'field_id' in self.parameter:
            new_field_id = self.parameter['field_id']
            self.move(new_field_id)

            self.card_data['move'] = self.check_field_type()

    def __pay_all_users(self):
        self.card_data["pay"] = 0

        for user_to_pay in PlayingUser.objects.filter(~Q(id=self.user.id)):
            self.card_data["pay"] += self.parameter["pay"]
            user_to_pay.budget += self.parameter["pay"]
            self.user.budget -= self.parameter["pay"]
            user_to_pay.save()

    def __pay_for_assets(self):
        self.card_data["pay"] = 0
        for asset in Asset.objects.filter(playingUser_id=self.user.id):
            number_of_houses = asset.estateNumber if asset else 0

            if number_of_houses == 5:
                # HOTEL
                self.user.budget -= self.parameter["hotel"]
                self.card_data["pay"] += self.parameter["hotel"]
            elif number_of_houses > 0:
                payed = self.parameter["house"] * number_of_houses
                self.user.budget -= payed
                self.card_data["pay"] += payed

    def __get_money_from_users(self):
        self.card_data["get"] = 0
        for user_to_pay in PlayingUser.objects.filter(~Q(id=self.user.id)):
            user_to_pay.budget -= self.parameter["get"]
            self.response["get"] += self.parameter["get"]
            self.card_data.budget += self.parameter["get"]


class UseGetOutOfJailCardView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlayingUserSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawid??owy u??ytkownik", status=403)

        if not (user.prison and self.user.prison["checked"]):
            return Response("U??ytkownik nie jest w wi??zieniu", status=403)

        if user.isActive and user.isPlaying:
            if user.get_out_of_jail_card > 0:
                user.get_out_of_jail_card -= 1
                user.prison = None
        else:
            return Response("U??ytkownik nie ma prawa ruchu", status=403)

        return Response("U??ytkownik wyszed?? z wi??zienia.")


class CountGetOutOfJailCardView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlayingUserSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawid??owy u??ytkownik", status=403)

        if user.isActive:
            return Response({"jail-card": user.get_out_of_jail_card})
        else:
            return Response("Podany u??ytkownik nie jest aktywny", status=406)


class LobbyView(TemplateView):
    template_name = "lobby.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class BoardView(ListAPIView):
    def get(self, request, *args, **kwargs):
        d = {}
        for obj in Field.objects.all():
            d[obj.pk] = {
                "name": obj.name,
                "id": obj.id,
                "type": obj.field_type.name,
                "price": obj.price,
                "zone": obj.zone.pk if obj.zone else None,
                "owner": None,
            }
        for user in PlayingUser.objects.filter(isActive=True):
            if "users" in d[user.field.pk]:
                d[user.field.pk]["users"].append(user.pk)
            else:
                d[user.field.pk]["users"] = [user.pk]

        for asset in Asset.objects.filter(playingUser__isActive=True):
            owner = User.objects.get(playing_users=asset.playingUser.pk)
            d[asset.field.pk]["owner"] = owner.username
            d[asset.field.pk]["isPledged"] = asset.isPledged
            d[asset.field.pk]["houses"] = (
                asset.estateNumber if asset.estateNumber else 0
            )

        return Response(d)


class FieldView(ListAPIView):
    def get(self, request, *args, **kwargs):

        try:
            estate = Estate.objects.get(field=self.kwargs["pk"])
        except Estate.DoesNotExist:
            return Response("")
        d = EstateSerializer(estate).data

        d["id"] = estate.field.pk
        d["name"] = estate.field.name
        d["type"] = estate.field.field_type.name
        d["price"] = estate.field.price
        d["zone"] = estate.field.zone.pk if estate.field.zone else None
        d["owner"] = None
        d["users"] = []

        for user in PlayingUser.objects.filter(isPlaying=True, field=estate.field):
            d["users"].append(user.pk)

        for asset in Asset.objects.filter(playingUser__isPlaying=True):
            d["owner"] = asset.playingUser.pk
            d["isPledged"] = asset.isPledged
            d["houses"] = asset.estateNumber if asset.estateNumber else 0

        return Response(d)


class BuyFieldView(CreateAPIView):
    """
    Active and playing user buying current standing field
    """

    permission_classes = [IsAuthenticated]
    queryset = None
    serializer_class = None

    def post(self, request, *args, **kwargs):
        try:
            user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawid??owy u??ytkownik", status=403)
        if user.isActive and user.isPlaying:
            field = user.field
            if Asset.objects.filter(field=field):
                return Response("Obecne pole jest zaj??te", status=403)
            if field.field_type.pk not in [7, 8, 9]:
                return Response(
                    "Nieprawid??owy typ pola " + field.field_type.name, status=403
                )
            if user.budget < field.price:
                return Response("Niewystarczaj??cy bud??et", status=403)
            user.budget -= field.price
            user.save()
            Asset.objects.create(field=field, playingUser=user)
            return Response("Kupiono pomy??lnie")

        else:
            return Response("U??ytkownik nie ma prawa zakupu", status=401)


class SellFieldView(DestroyAPIView):
    """
    Active and playing user sell field (id in params)
    """

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawid??owy u??ytkownik", status=403)
        if user.isActive and user.isPlaying:
            try:
                field = Field.objects.get(pk=self.kwargs["pk"])
            except Field.DoesNotExist:
                return Response("Nieprawid??owe pole", status=403)

            try:
                asset = Asset.objects.get(field=field, playingUser=user)
            except Asset.DoesNotExist:
                return Response("Nieprawid??owy w??a??ciciel pola", status=403)

            if field.field_type.pk != 7:
                houses = 0
            else:
                houses = asset.estateNumber * field.zone.price_per_house
            if asset.isPledged:
                user.budget += field.price / 2 + houses
                user.save()
                asset.delete()
            else:
                user.budget += field.price + houses
                user.save()
                asset.delete()

            return Response("Sprzedano pomy??lnie")

        else:
            return Response("U??ytkownik nie ma prawa sprzeda??y", status=401)


class PledgeFieldView(UpdateAPIView):
    """
    Active and playing user pledge field
    """

    permission_classes = [IsAuthenticated]
    serializer_class = FieldSerializer

    def put(self, request, *args, **kwargs):
        try:
            user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawid??owy u??ytkownik", status=403)
        if user.isActive and user.isPlaying:
            validated_data = self.serializer_class(request.data).data
            try:
                field = Field.objects.get(pk=validated_data["field"])
            except Field.DoesNotExist:
                return Response("B????dne pole", status=403)

            if field.field_type.pk not in [7, 8, 9]:
                return Response(
                    "Nieprawid??owy typ pola " + field.field_type.name, status=403
                )
            try:
                asset = Asset.objects.get(field=field, playingUser=user)
                if asset.isPledged:
                    return Response("Obecne pole jest ju?? zastawione", status=403)
                user.budget += field.price / 2
                user.save()
                asset.isPledged = True
                asset.save()
                return Response("Zastawiono pomy??lnie")
            except Asset.DoesNotExist:
                return Response("Pole nie nale??y do u??ytkownika", status=403)

        else:
            return Response("U??ytkownik nie ma prawa zastawiania", status=401)


class UnPledgeFieldView(UpdateAPIView):
    """
    Active and playing user reverse pledge field
    """

    permission_classes = [IsAuthenticated]
    serializer_class = FieldSerializer

    def put(self, request, *args, **kwargs):
        try:
            user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawid??owy u??ytkownik", status=403)
        if user.isActive and user.isPlaying:
            validated_data = self.serializer_class(request.data).data
            try:
                field = Field.objects.get(pk=validated_data["field"])
            except Field.DoesNotExist:
                return Response("B????dne pole", status=403)

            if field.field_type.pk not in [7, 8, 9]:
                return Response(
                    "Nieprawid??owy typ pola " + field.field_type.name, status=403
                )
            try:
                asset = Asset.objects.get(field=field, playingUser=user)
                if asset.isPledged is False:
                    return Response("Obecne pole nie jest zastawione", status=403)
                if user.budget < field.price:
                    return Response("Niewystarczaj??cy bud??et", status=403)
                user.budget -= field.price / 2
                user.save()
                asset.isPledged = False
                asset.save()
                return Response("Zastawienie usuni??te pomy??lnie")
            except Asset.DoesNotExist:
                return Response("Pole nie nale??y do u??ytkownika", status=403)

        else:
            return Response("U??ytkownik nie ma prawa usuwania zastawienia", status=401)


class BuyEstateFieldView(CreateAPIView):
    """
    Active and playing user buying houses for field
    """

    permission_classes = [IsAuthenticated]
    serializer_class = FieldEstateSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawid??owy u??ytkownik", status=403)
        if user.isActive and user.isPlaying:
            validated_data = self.serializer_class(request.data).data
            try:
                field = Field.objects.get(pk=validated_data["field"])
            except Field.DoesNotExist:
                return Response("B????dne pole", status=403)

            if field.field_type.pk != 7:
                return Response(
                    "Nieprawid??owy typ pola " + field.field_type.name, status=403
                )
            try:
                asset = Asset.objects.get(field=field, playingUser=user)
                if asset.isPledged is True:
                    return Response("Obecne pole jest zastawione", status=403)
                number_of_houses = validated_data["number_of_houses"]
                if (
                        number_of_houses not in range(1, 6)
                        or asset.estateNumber + number_of_houses > 5
                ):
                    return Response("B????dna ilo???? domk??w", status=403)
                if user.budget < field.zone.price_per_house * number_of_houses:
                    return Response("Niewystarczaj??cy bud??et", status=403)
                user.budget -= field.zone.price_per_house * number_of_houses
                user.save()
                asset.estateNumber += number_of_houses
                asset.save()
                return Response("Zakupiono pomy??lnie")
            except Asset.DoesNotExist:
                return Response("Pole nie nale??y do u??ytkownika", status=403)

        else:
            return Response("U??ytkownik nie ma prawa usuwania zastawienia", status=401)


class SellEstateFieldView(CreateAPIView):
    """
    Active and playing user sell houses for field
    """

    permission_classes = [IsAuthenticated]
    serializer_class = FieldEstateSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawid??owy u??ytkownik", status=403)
        if user.isActive and user.isPlaying:
            validated_data = self.serializer_class(request.data).data
            try:
                field = Field.objects.get(pk=validated_data["field"])
            except Field.DoesNotExist:
                return Response("B????dne pole", status=403)

            if field.field_type.pk != 7:
                return Response(
                    "Nieprawid??owy typ pola " + field.field_type.name, status=403
                )
            try:
                asset = Asset.objects.get(field=field, playingUser=user)
                if asset.isPledged is True:
                    return Response("Obecne pole jest zastawione", status=403)
                number_of_houses = validated_data["number_of_houses"]
                if (
                        number_of_houses not in range(1, 6)
                        or asset.estateNumber - number_of_houses < 0
                ):
                    return Response("B????dna ilo???? domk??w", status=403)

                user.budget += field.zone.price_per_house * number_of_houses
                user.save()
                asset.estateNumber -= number_of_houses
                asset.save()
                return Response("Sprzedano pomy??lnie")
            except Asset.DoesNotExist:
                return Response("Pole nie nale??y do u??ytkownika", status=403)

        else:
            return Response("U??ytkownik nie ma prawa usuwania zastawienia", status=401)


class TransactionsView(ListCreateAPIView):
    serializer_class = CreateTransactionSerializer
    queryset = Transaction.objects.all()

    def get(self, request, *args, **kwargs):
        auth_queryset = Transaction.objects.filter(
            Q(seller=self.request.user, isBuyingOffer=False)
            | Q(buyer=self.request.user, isBuyingOffer=True)
        )
        send_by_auth = TransactionListSerializer(auth_queryset, many=True).data
        others_queryset = Transaction.objects.filter(
            Q(seller=self.request.user, isBuyingOffer=True)
            | Q(buyer=self.request.user, isBuyingOffer=False)
        )
        send_by_others = TransactionListSerializer(others_queryset, many=True).data
        return Response(
            {"send_by_auth": send_by_auth, "send_by_others": send_by_others}
        )

    def post(self, request, *args, **kwargs):
        if request.data["isBuyingOffer"] == "true":
            request.data["buyer"] = request.user.id
        else:
            request.data["seller"] = request.user.id
        if  request.data["buyer"] == request.data["seller"]:
            return Response("Posiadasz ju?? to pole.",status=403)
        print(request.data)
        return super().post(request, *args, **kwargs)


class TransactionUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        try:
            transaction = self.get_object(pk)
            buyer = PlayingUser.objects.filter(user=transaction.buyer).first()
            seller = PlayingUser.objects.filter(user=transaction.seller).first()
            if (
                    Asset.objects.filter(
                        playingUser=seller, field=transaction.field
                    ).count()
                    == 0
                    or transaction.price > buyer.budget
            ):
                print(
                    Asset.objects.filter(
                        playingUser=seller, field=transaction.field
                    ).count()
                )
                return Response("Przekroczono bud??et lub sprzedaj??cy nie posiada ju?? tego pola.", status=403)

            buyer.budget -= transaction.price
            buyer.save()
            seller.budget += transaction.price
            seller.save()
            seller_asset = Asset.objects.filter(
                playingUser=seller, field=transaction.field
            ).first()
            seller_asset.playingUser = buyer
            seller_asset.save()
            transaction.finished = True
            transaction.save()
            return Response("Transakcja zosta??a zako??czona", status=200)
        except Exception as e:
            return Response("Nie mo??na dokona?? transakcji.", status=500)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
