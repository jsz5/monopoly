from api.models import PlayingUser, Estate, Field, Card, Asset
from rest_framework import serializers

# from django.apps import apps
from api.models import Transaction
from django.contrib.auth.models import User

from api.models import Asset


class PlayingUserSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = PlayingUser
        depth = 1
        fields = ["id", "user_id", "place", "isPlaying", "isActive", "budget", "user", "dice", "prison", "get_out_of_jail_card"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class TransactionListSerializer(serializers.ModelSerializer):
    seller = UserSerializer()
    buyer = UserSerializer()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "price",
            "isBuyingOffer",
            "seller",
            "buyer",
            "field_id",
            "finished",
        ]


class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "price",
            "isBuyingOffer",
            "buyer",
            "seller",
            "field",
            "finished",
        ]

    def validate(self, attr):
        auth = self.context["request"].user
        auth_playing = PlayingUser.objects.get(user=auth)
        buyer = PlayingUser.objects.filter(user=attr["buyer"]).first()
        seller = PlayingUser.objects.filter(user=attr["seller"]).first()

        if attr["isBuyingOffer"]:
            if auth_playing != buyer:
                raise serializers.ValidationError({"buyer": "Błędny użytkownik"})
            if attr["price"] > auth_playing.budget:
                raise serializers.ValidationError(
                    {"price": "Twój budżet jest zbyt mały."}
                )

            if seller is None:
                raise serializers.ValidationError({"seller": "Wystąpił błąd"})
            if (
                Asset.objects.filter(playingUser=seller, field_id=attr["field"]).count()
                == 0
            ):
                raise serializers.ValidationError(
                    {
                        "seller": f"Gracz {seller.user.username} nie posiada pola {attr['field'].id}"
                    }
                )

        else:
            if auth_playing != seller:
                raise serializers.ValidationError({"buyer": "Błędny użytkownik"})
            if (
                Asset.objects.filter(
                    playingUser=auth_playing, field_id=attr["field"]
                ).count()
                == 0
            ):
                raise serializers.ValidationError(
                    {"seller": f"Nie posiadasz pola {attr['field'].id}"}
                )

        return attr

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.finished = True
        instance.save()
        return instance


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["isPledged", "field_id", "playingUser_id", "estateNumber"]


class EstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estate
        fields = [
            "id",
            "fee_zero_houses",
            "fee_one_house",
            "fee_two_houses",
            "fee_three_houses",
            "fee_four_houses",
            "fee_five_houses",
        ]


class FieldSerializer(serializers.ModelSerializer):
    field = serializers.IntegerField()

    class Meta:
        model = Field
        fields = ["field"]


class FieldEstateSerializer(serializers.ModelSerializer):
    field = serializers.IntegerField()
    number_of_houses = serializers.IntegerField()

    class Meta:
        model = Field
        fields = ["field", "number_of_houses"]


class CardSerializer(serializers.ModelSerializer):
    action = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Card
        fields = ["description", "parameter", "action_id", "action"]