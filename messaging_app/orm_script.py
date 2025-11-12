
import os
import django

# Tell Django where to find settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')
django.setup()


from django.contrib.auth import get_user_model
from django.db import connection
from chats.models import Conversation, Messages


User = get_user_model()
def run():
    user = User.objects.get(username="Oge123")
    conversation = Conversation.objects.filter(name__icontains="Movie Nights").first()
    message = Messages.objects.create(sender=user, conversation_id=conversation.conversation_id, message="Welcome #everyone!")
    print(connection.queries)
  


if __name__ == '__main__':
    run()