
import os
import django

# Tell Django where to find settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')
django.setup()


from django.contrib.auth import get_user_model
from django.db import connection


User = get_user_model()
def run():
    
    print(connection.queries)


if __name__ == '__main__':
    run()