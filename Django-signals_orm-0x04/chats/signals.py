from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Conversation
from django.contrib.auth import get_user_model
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


User = get_user_model()
@receiver(post_save, sender=Conversation)
def add_user_to_conversation_signal(sender, instance, created, **kwargs):
    """ Authomatically adds the user who created the conversation once the conversation is created """
    if isinstance(instance, Conversation) and created:
       user = instance.user
       if user and isinstance(user, User):
           instance.participants.add(user)
    
    logger.info(f"Added {user.username} in the list of participants in a conversation title {instance.name}")
