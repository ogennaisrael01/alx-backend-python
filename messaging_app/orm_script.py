
import os
import django

# Tell Django where to find settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')
django.setup()


from django.contrib.auth import get_user_model
from django.db import connection
from chats.models import Conversation, Message
from django.core.management.utils import get_random_secret_key


User = get_user_model()

def run():
   print(get_random_secret_key())
  


if __name__ == '__main__':
    run()