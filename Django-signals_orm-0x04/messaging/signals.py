from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
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

@receiver(post_delete, sender=Message, weak=False, dispatch_uid="Delete a message")
def delete_message_signal(sender, instance, **kwargs):
    print(f"Message deleted by {instance.sender} at ({instance.timestamp})")
    # No need to delete again; the object is already deleted.

