from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from messaging.models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message, weak=False, dispatch_uid="Send a message")
def message_signal(sender, instance, created, **kwargs):
    print("Signal fired....")
    if created:
        print(f"Message created by {instance.sender} to {instance.receiver} at {instance.timestamp}")
        Notification.objects.create(
            user=instance.receiver,
            notification=f"New message from {instance.sender}",
            content=str(instance)  # or instance.content if that's what you want
        )

@receiver(pre_save, sender=Message, weak=True, dispatch_uid="edit message")
def edit_message_signal(sender, instance, **kwargs):
    if instance.pk:
        # edit an existing message
        print(f"Message edited by {instance.sender} at {instance.timestamp}")
        instance.edited = True
        MessageHistory.objects.create(
            message=instance,
            edited_by=instance.sender
        )
    else:
        print(f"Message created by {instance.sender} to {instance.receiver} at {instance.timestamp}")

@receiver(post_delete, sender=User, weak=False, dispatch_uid="Delete user messages")
def delete_message_signal(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    print(f"Messages deleted for user {instance.username}")

