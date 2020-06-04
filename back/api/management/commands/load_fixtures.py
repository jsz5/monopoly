from django.core import management
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from api.models import Action, FieldType, Zone, Field, Estate, Card


class Command(BaseCommand):
    help = """Command loads fixtures."""

    def handle(self, *args, **options):
        User.objects.all().delete()
        Action.objects.all().delete()
        FieldType.objects.all().delete()
        Zone.objects.all().delete()
        Field.objects.all().delete()
        Estate.objects.all().delete()
        Card.objects.all().delete()

        fixtures = [
            "users.json",
            "action.json",
            "fieldtype.json",
            "zone.json",
            "field.json",
            "estate.json",
            "card.json",
        ]

        for fixture in fixtures:
            management.call_command("loaddata", "fixtures/" + fixture)
