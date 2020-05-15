from api.models import PlayingUser
from rest_framework import serializers


class PlayingUserSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
     )
    class Meta:
        model = PlayingUser
        depth = 1
        fields = ["id", "user_id", "place", "isPlaying", "isActive","budget", "user"]
