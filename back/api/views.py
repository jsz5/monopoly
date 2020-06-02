import json

from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib import auth
from rest_framework.authtoken.models import Token
from api.models import PlayingUser, FieldType, Field, Messages, Asset, Estate
from rest_auth.serializers import LoginSerializer
from rest_auth.views import LogoutView
import random

from django.http import HttpResponse

from api.serializers import PlayingUserSerializer, EstateSerializer, FieldSerializer, FieldEstateSerializer

from django.views.generic import CreateView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
            return Response({"show_board": True, "message": "Gra rozpoczęta."})

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
                return True  # gracze z tabeli mogą rozpocząć grę (przycisk ROZPOCZNIJ GRĘ jest dostępny) - event
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


class DiceRollView(ListAPIView):
    """
    Active and playing user dice roll, function modify standing field
    """

    def get(self, request, *args, **kwargs):
        dice = random.randint(1, 12)
        try:
            user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawidłowy użytkownik", status=403)
        if user.isActive and user.isPlaying:
            field_count = Field.objects.all().count()
            if int(user.field.pk) + dice > field_count:
                user.budget += 2000
                field = Field.objects.get(pk=int(user.field.pk + dice - field_count))
            else:
                field = Field.objects.get(pk=int(user.field.pk + dice))

            try:
                asset = Asset.objects.get(field=field)
                if asset.isPledged:
                    asset = None
            except Asset.DoesNotExist:
                asset = None

            # action
            if field.field_type == 3:
                # card
                pass
            elif field.field_type == 4:
                # pay
                user.budget -= 2000
            elif field.field_type == 5:
                # go to jail
                field = Field.objects.get(field_type=5)
            elif field.field_type == 7:
                #     normal
                if asset and asset.playingUser != user:
                    estate = Estate.objects.get(field=field)
                    if asset.estateNumber == 0:
                        user.budget -= estate.fee_zero_houses
                    elif asset.estateNumber == 1:
                        user.budget -= estate.fee_one_house
                    elif asset.estateNumber == 2:
                        user.budget -= estate.fee_two_houses
                    elif asset.estateNumber == 3:
                        user.budget -= estate.fee_three_houses
                    elif asset.estateNumber == 4:
                        user.budget -= estate.fee_four_houses
                    elif asset.estateNumber == 5:
                        user.budget -= estate.fee_five_houses
            elif field.field_type == 8:
                #     power plant
                # todo fix it
                if asset and asset.playingUser != user:
                    user.budget -= dice * 200
            elif field.field_type == 9:
                #     transport
                # todo fix it
                if asset and asset.playingUser != user:
                    user.budget -= 2000

            if user.budget < 0:
                for asset in Asset.objects.filter(playingUser=user):
                    user.budget += asset.price + asset.estateNumber * asset.field.zone.price_per_house
                    asset.delete()
                    if user.budget > 0:
                        break

            if user.budget < 0:
                user.isActive = False
                return Response("Przegrana gra")

            user.field = field
            user.save()
            # message = {"user": user.id, "field": user.place}
            # Messages(type="move", parameter=message).save()
            return Response({"number": dice, 'new_field': user.field.name})
        else:
            return Response("Użytkownik nie ma prawa ruchu", status=403)


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
                "type": obj.field_type.name,
                "price": obj.price,
                "zone": obj.zone.pk if obj.zone else None,
                "owner": None,
            }
        for user in PlayingUser.objects.filter(isPlaying=True):
            if "users" in d[user.field.pk]:
                d[user.field.pk]["users"].append(user.pk)
            else:
                d[user.field.pk]["users"] = [user.pk]

        for asset in Asset.objects.filter(playingUser__isPlaying=True):
            d[asset.field.pk]["owner"] = asset.playingUser.pk
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

    def post(self, request, *args, **kwargs):
        try:
            user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawidłowy użytkownik", status=403)
        if user.isActive and user.isPlaying:
            field = user.field
            if Asset.objects.filter(field=field):
                return Response("Obecne pole jest zajęte", status=403)
            if field.field_type.pk not in [7, 8, 9]:
                return Response(
                    "Nieprawidłowy typ pola " + field.field_type.name, status=403
                )
            if user.budget < field.price:
                return Response("Niewystarczający budżet", status=403)
            user.budget -= field.price
            user.save()
            Asset.objects.create(field=field, playingUser=user)
            return Response("Kupiono pomyślnie")

        else:
            return Response("Użytkownik nie ma prawa zakupu", status=401)


class SellFieldView(DestroyAPIView):
    """
    Active and playing user sell field (id in params)
    """

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            user = PlayingUser.objects.get(user=request.user)
        except PlayingUser.DoesNotExist:
            return Response("Nieprawidłowy użytkownik", status=403)
        if user.isActive and user.isPlaying:
            try:
                field = Field.objects.get(pk=self.kwargs["pk"])
            except Field.DoesNotExist:
                return Response("Nieprawidłowe pole", status=403)

            try:
                asset = Asset.objects.get(field=field, playingUser=user)
            except Asset.DoesNotExist:
                return Response("Nieprawidłowy właściciel pola", status=403)

            if field.field_type.pk != 7:
                houses = 0
            else:
                houses = asset.estateNumber * field.zone.price_per_house
            if asset.isPledged:
                user.budget += (
                        field.price / 2 + houses
                )
                user.save()
                asset.delete()
            else:
                user.budget += (
                        field.price + houses
                )
                user.save()
                asset.delete()

            return Response("Sprzedano pomyślnie")

        else:
            return Response("Użytkownik nie ma prawa sprzedaży", status=401)


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
            return Response("Nieprawidłowy użytkownik", status=403)
        if user.isActive and user.isPlaying:
            validated_data = self.serializer_class(request.data).data
            try:
                field = Field.objects.get(pk=validated_data["field"])
            except Field.DoesNotExist:
                return Response("Błędne pole", status=403)

            if field.field_type.pk not in [7, 8, 9]:
                return Response(
                    "Nieprawidłowy typ pola " + field.field_type.name, status=403
                )
            try:
                asset = Asset.objects.get(field=field, playingUser=user)
                if asset.isPledged:
                    return Response("Obecne pole jest już zastawione", status=403)
                user.budget += field.price / 2
                user.save()
                asset.isPledged = True
                asset.save()
                return Response("Zastawiono pomyślnie")
            except Asset.DoesNotExist:
                return Response("Pole nie należy do użytkownika", status=403)

        else:
            return Response("Użytkownik nie ma prawa zastawiania", status=401)


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
            return Response("Nieprawidłowy użytkownik", status=403)
        if user.isActive and user.isPlaying:
            validated_data = self.serializer_class(request.data).data
            try:
                field = Field.objects.get(pk=validated_data["field"])
            except Field.DoesNotExist:
                return Response("Błędne pole", status=403)

            if field.field_type.pk not in [7, 8, 9]:
                return Response(
                    "Nieprawidłowy typ pola " + field.field_type.name, status=403
                )
            try:
                asset = Asset.objects.get(field=field, playingUser=user)
                if asset.isPledged is False:
                    return Response("Obecne pole nie jest zastawione", status=403)
                if user.budget < field.price:
                    return Response("Niewystarczający budżet", status=403)
                user.budget -= field.price / 2
                user.save()
                asset.isPledged = False
                asset.save()
                return Response("Zastawienie usunięte pomyślnie")
            except Asset.DoesNotExist:
                return Response("Pole nie należy do użytkownika", status=403)

        else:
            return Response("Użytkownik nie ma prawa usuwania zastawienia", status=401)


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
            return Response("Nieprawidłowy użytkownik", status=403)
        if user.isActive and user.isPlaying:
            validated_data = self.serializer_class(request.data).data
            try:
                field = Field.objects.get(pk=validated_data["field"])
            except Field.DoesNotExist:
                return Response("Błędne pole", status=403)

            if field.field_type.pk != 7:
                return Response(
                    "Nieprawidłowy typ pola " + field.field_type.name, status=403
                )
            try:
                asset = Asset.objects.get(field=field, playingUser=user)
                if asset.isPledged is True:
                    return Response("Obecne pole jest zastawione", status=403)
                number_of_houses = validated_data["number_of_houses"]
                if number_of_houses not in range(1, 6) or asset.estateNumber + number_of_houses > 5:
                    return Response("Błędna ilość domków", status=403)
                if user.budget < field.zone.price_per_house * number_of_houses:
                    return Response("Niewystarczający budżet", status=403)
                user.budget -= field.zone.price_per_house * number_of_houses
                user.save()
                asset.estateNumber += number_of_houses
                asset.save()
                return Response("Zakupiono pomyślnie")
            except Asset.DoesNotExist:
                return Response("Pole nie należy do użytkownika", status=403)

        else:
            return Response("Użytkownik nie ma prawa usuwania zastawienia", status=401)


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
            return Response("Nieprawidłowy użytkownik", status=403)
        if user.isActive and user.isPlaying:
            validated_data = self.serializer_class(request.data).data
            try:
                field = Field.objects.get(pk=validated_data["field"])
            except Field.DoesNotExist:
                return Response("Błędne pole", status=403)

            if field.field_type.pk != 7:
                return Response(
                    "Nieprawidłowy typ pola " + field.field_type.name, status=403
                )
            try:
                asset = Asset.objects.get(field=field, playingUser=user)
                if asset.isPledged is True:
                    return Response("Obecne pole jest zastawione", status=403)
                number_of_houses = validated_data["number_of_houses"]
                if number_of_houses not in range(1, 6) or asset.estateNumber - number_of_houses < 0:
                    return Response("Błędna ilość domków", status=403)

                user.budget += field.zone.price_per_house * number_of_houses
                user.save()
                asset.estateNumber -= number_of_houses
                asset.save()
                return Response("Sprzedano pomyślnie")
            except Asset.DoesNotExist:
                return Response("Pole nie należy do użytkownika", status=403)

        else:
            return Response("Użytkownik nie ma prawa usuwania zastawienia", status=401)
