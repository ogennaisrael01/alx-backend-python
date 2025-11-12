
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
    conversation = Conversation.objects.filter(name__icontains="Startup Founders").first()
    # conversation.participants.add(user)
    print(user.id)
    print(conversation.conversation_id)

    print(connection.queries)
  


if __name__ == '__main__':
    run()