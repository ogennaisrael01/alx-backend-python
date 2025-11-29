
import os
import django

# Tell Django where to find settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')
django.setup()


from django.contrib.auth import get_user_model
from django.db import connection
from chats.models import Conversation, Message


User = get_user_model()
def run():
    message = Message.objects.get(pk="60599db8-8abd-47dc-97dd-951dd2f7045d")
    nested_message = Message.objects.filter(parent_message=message).first()
    print(nested_message.pk)
    print(connection.queries)
  


if __name__ == '__main__':
    run()