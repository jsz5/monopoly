from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status
from api.models import User, PlayingUser, FieldType, Field, Asset, Estate, Card
from django.urls import reverse
from rest_framework.test import force_authenticate
from api.views import DiceRollView
from django.db.models import Q


class LoginTestCase(APITestCase):
    """ Test module for POST login API """
    fixtures = ["fixtures/users.json"]

    def test_login(self):
        data = {
          "username": "user1",
          "email": "",
          "password": "123456"
        }
        url = "/api/login/"
        response = self.client.post(url, data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CardThreeForTwoUsersTestCase(TestCase):
    fixtures = [
        "fixtures/users.json",
        "fixtures/action.json",
        "fixtures/fieldtype.json",
        "fixtures/zone.json",
        "fixtures/field.json",
        "fixtures/estate.json",
        "fixtures/card.json",
    ]

    def setUp(self):
        user = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        playing_user = PlayingUser(isActive=True, isPlaying=True, budget=6000, user=user)
        playing_user.save()
        playing_user1 = PlayingUser(isActive=True, isPlaying=False, budget=6000, user=user2)
        playing_user1.save()
        self.dice_roll_view = DiceRollView()
        self.dice_roll_view.user = playing_user
        self.dice_roll_view.response = dict()
        self.dice_roll_view.field = Field.objects.get(pk=3)
        self.dice_roll_view.dice = 1
        self.dice_roll_view.asset = None

    def test_move(self):
        field_id = 4
        self.dice_roll_view.move(field_id)
        self.assertEqual(self.dice_roll_view.user.field_id, field_id)
        self.assertEqual(self.dice_roll_view.field, Field.objects.get(pk=field_id))

    def test_card_2(self):
        response = self.dice_roll_view.card(2)

        self.assertEqual(self.dice_roll_view.user.budget, 5500)
        self.assertEquals(PlayingUser.objects.filter(~Q(id=self.dice_roll_view.user.id)).first().budget, 6500)
        self.assertGreaterEqual(response.items(), {"pay": 500, "action_id": 4}.items())

    def test_card_3(self):
        """Idź na najbliższy Dworzec kolejowy"""
        response = self.dice_roll_view.card(3)

        self.assertEqual(self.dice_roll_view.field.pk, 6)
        self.assertGreaterEqual(response.items(), {"action_id": 2}.items())

    def test_card_6(self):
        """ Przeprowadź remont generalny wszystkich swoich nieruchomości: Zapłać za każdy dom M 250. Zapłać za każdy hotel M 1000 """
        budget = self.dice_roll_view.user.budget
        Asset(isPledged=False, field_id=2, playingUser_id=self.dice_roll_view.user.id, estateNumber=4).save()
        Asset(isPledged=False, field_id=12, playingUser_id=self.dice_roll_view.user.id, estateNumber=2).save()
        Asset(isPledged=False, field_id=3, playingUser_id=self.dice_roll_view.user.id, estateNumber=5).save()
        response = self.dice_roll_view.card(6)

        self.assertEqual(self.dice_roll_view.user.budget, budget-4*250-2*250-1000)
        self.assertEqual(response['pay'], 4*250+2*250+1000)

    def test_card_9(self):
        """Zapłać grzywne - M 1500"""
        budget = self.dice_roll_view.user.budget
        self.dice_roll_view.card(9)

        self.assertEqual(self.dice_roll_view.user.budget, budget-1500)

    def test_card_10(self):
        """Cofnij się o trzy pola."""
        self.dice_roll_view.field = Field.objects.get(pk=3)

        self.dice_roll_view.card(10)
        self.assertEqual(self.dice_roll_view.field.pk, 40)
        self.assertEqual(self.dice_roll_view.user.field_id, 40)


# class

# class PowerPlantTestCase(TestCase):
#     fixtures = [
#         "fixtures/users.json",
#         "fixtures/action.json",
#         "fixtures/fieldtype.json",
#         "fixtures/zone.json",
#         "fixtures/field.json",
#         "fixtures/estate.json",
#         "fixtures/card.json",
#     ]
#
#     def setUp(self):
#         user = User.objects.get(pk=1)
#         user2 = User.objects.get(pk=2)
#         playing_user = PlayingUser(isActive=True, isPlaying=True, budget=6000, user=user)
#         playing_user.save()
#         playing_user1 = PlayingUser(isActive=True, isPlaying=False, budget=6000, user=user2)
#         playing_user1.save()
#         self.dice_roll_view = DiceRollView()
#         self.dice_roll_view.user = playing_user
#         self.dice_roll_view.response = dict()
#         self.dice_roll_view.field = Field.objects.get(pk=3)
#         self.dice_roll_view.dice = 1
#         self.dice_roll_view.asset = None


# class NormalTestCase(TestCase):
