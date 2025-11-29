
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
    message = Message.objects.get(message_id="1765885e-f3de-4bfb-a636-bdb3c4b10656")
    histories = message.message_history.all()
    for history in histories[:1]:
        print(history.message_body_history)

    print(connection.queries)
  


if __name__ == '__main__':
    run()