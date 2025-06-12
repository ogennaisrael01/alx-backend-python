from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from messaging.models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message, weak=False, dispatch_uid="Send a message")
def  message_signal(sender, instance, created, **kwargs):
    print("Signal fired....")
    if created:
        print(f"Message created by {instance.sender} to {instance.reciever} at {instance.timestamp}")
        Notification.objects.create(
            user=instance.reciever,
            notification=f"New message from {instance.sender}",
            content=instance
        )
    
@receiver(pre_save, sender=Message, weak=True, dispatch="edit message")
def edit_message_signal(sender, instance, **kwargs):
    if instance.pk:
        # edit an existing message
        print(f"message edited by {instance.sender} at {instance.timestamp}")
        instance.edited = True
        MessageHistory.objects.create(
            message=instance,
            edited_by=instance.sender
        )
    else:
        print(f"Message created by {instance.sender} to {instance.reciever} at {instance.timestamp}")