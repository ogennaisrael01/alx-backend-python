
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
    conversation = Conversation.objects.filter(conversation_id__iexact="485c74af-11bb-44e7-8d46-a5ec49237e69").first()
    if user in conversation.participants.all():
        print(conversation.participants.all())
        print(conversation.messages.all()[:5])
        return 
    print("error")

    print(connection.queries)
  


if __name__ == '__main__':
    run()