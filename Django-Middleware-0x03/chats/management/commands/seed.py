from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from chats.models import Conversation, Messages

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        # Create users
        user1, _ = User.objects.get_or_create(username='alice', email='alice@example.com')
        user1.set_password('password123')
        user1.save()
        user2, _ = User.objects.get_or_create(username='bob', email='bob@example.com')
        user2.set_password('password123')
        user2.save()

        # Create a conversation
        conv, _ = Conversation.objects.get_or_create(title='Test Conversation')
        conv.participants.set([user1, user2])
        conv.save()

        # Create messages
        Messages.objects.get_or_create(conversation=conv, sent_by=user1, message_body='Hello Bob!')
        Messages.objects.get_or_create(conversation=conv, sent_by=user2, message_body='Hi Alice!')

        self.stdout.write(self.style.SUCCESS('Database seeded!'))