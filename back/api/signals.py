from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from api.models import Messages


@receiver(post_save, sender=Messages)
def send_message(sender, instance, **kwargs):
    """
    todo: wysyłanie eventu o nowym message
    """
    pass
