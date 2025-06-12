from django.db.models.signals import post_save
from django.dispatch import receiver
from messaging.models import Message, Notification

@receiver(post_save, sender=Message, weak=False, dispatch_uid="Send a message")
def  message_signal(sender, instance, created, **kwargs):
    print("Signal fired....")
    if created:
        print(f"Message created by {instance.sender} to {instance.reciever} at {instance.timestamp}")
        Notification.objects.create(
            user=instance.reciever,
            notification=f"New message from {instance.sender}",
            content=instance.content
        )
    