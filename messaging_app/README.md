# Messaging App

A Django-based messaging application with REST API endpoints for managing users, conversations, and messages.

## Features

- Custom user model with phone number support
- Create and manage conversations between users
- Send and retrieve messages within conversations
- RESTful API using Django REST Framework
- Admin interface for managing users, conversations, and messages

## Project Structure

```
manage.py
chats/
    admin.py
    apps.py
    models.py
    serializers.py
    tests.py
    views.py
    migrations/
messaging_app/
    settings.py
    urls.py
    wsgi.py
    asgi.py
```

## Setup

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd messaging_app
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Apply migrations:**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser:**
   ```sh
   python manage.py createsuper
   
   ```

5. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

## API Endpoints

- `/api/conversation/` - CRUD for conversations
- `/api/messages/` - CRUD for messages

## Admin

Access the Django admin at `/admin/`.

## License

Educational purposes
