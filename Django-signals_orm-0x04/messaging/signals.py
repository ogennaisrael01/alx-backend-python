from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from chats.models import Conversation, Message, MessageHistory
from django.contrib.auth import get_user_model
import logging
from .models import Notification
from datetime import datetime

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



@receiver(post_save, sender=Message)
def notify_users_signal(sender, instance, created, **kwargs):
    " send out notification "
    if isinstance(instance, Message) and created:
        participants = instance.conversation.participants.all() # Notify all users inside the conversation when a message is created
        message = instance.message_body
        notification = Notification.objects.create(
                    content = message,
                    sender=instance.sender,
                    message=instance        
        )

        if notification:
            receivers = notification.receiver.all()
            for participant in participants:
                if participant in receivers:
                    continue
                notification.receiver.add(participant)

    logger.info(f"{instance.sender.username} sent a message: {instance.message_body}")


@receiver(pre_save, sender=Message)
def save_message_to_history_before_edit(sender, instance, **kwargs):
    if not instance.pk:
        return 
    previous_message = Message.objects.filter(message_id=instance.pk).first()
    if previous_message:
        message_history = MessageHistory.objects.create(
            message=previous_message,
            edited_by=instance.sender,
            message_body_history=previous_message.message_body
        )
    logger.info(f"message updated by {instance.sender.username}. message: {instance.message_body}")




