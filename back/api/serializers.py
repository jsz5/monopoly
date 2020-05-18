from api.models import PlayingUser, Estate
from rest_framework import serializers
# from django.apps import apps


class PlayingUserSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = PlayingUser
        depth = 1
        fields = ["id", "user_id", "place", "isPlaying", "isActive", "budget", "user"]


class EstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estate
        fields = ["id", "fee_zero_houses", "fee_one_house", "fee_two_houses", "fee_three_houses", "fee_four_houses",
                  "fee_five_houses"]
