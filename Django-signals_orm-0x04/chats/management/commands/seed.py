from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ...models import Conversation
import random
import uuid

User = get_user_model()

class Command(BaseCommand):
    help = "Populates database db"

    def handle(self, *args, **options):
        

        users_data = [
            {
                "email": "ogennaisrael@gmail.com",
                "password": "0987poiu",
                "username": "Oge123",
                "first_name": "Ogenna",
                "last_name": "Israel",
                "role": "HOST"
            },
            {
                "email": "amanda.bright@gmail.com",
                "password": "pass1234",
                "username": "AmandaB",
                "first_name": "Amanda",
                "last_name": "Bright",
                "role": "GUEST"
            },
            {
                "email": "john.doe@gmail.com",
                "password": "doe5678",
                "username": "JohnD",
                "first_name": "John",
                "last_name": "Doe",
                "role": "HOST"
            },
            {
                "email": "lucy.adebayo@yahoo.com",
                "password": "lucy@123",
                "username": "LucyA",
                "first_name": "Lucy",
                "last_name": "Adebayo",
                "role": "GUEST"
            },
            {
                "email": "michael.okoro@gmail.com",
                "password": "mike9988",
                "username": "MikeO",
                "first_name": "Michael",
                "last_name": "Okoro",
                "role": "HOST"
            },
            {
                "email": "chidera.nwosu@gmail.com",
                "password": "dera4567",
                "username": "ChiN",
                "first_name": "Chidera",
                "last_name": "Nwosu",
                "role": "GUEST"
            },
            {
                "email": "emma.williams@gmail.com",
                "password": "emma0000",
                "username": "EmmaW",
                "first_name": "Emma",
                "last_name": "Williams",
                "role": "HOST"
            },
            {
                "email": "tony.adams@gmail.com",
                "password": "tony7890",
                "username": "TonyA",
                "first_name": "Tony",
                "last_name": "Adams",
                "role": "GUEST"
            },
            {
                "email": "grace.uzoma@gmail.com",
                "password": "grace@456",
                "username": "GraceU",
                "first_name": "Grace",
                "last_name": "Uzoma",
                "role": "HOST"
            },
            {
                "email": "brian.kalu@gmail.com",
                "password": "brian9876",
                "username": "BrianK",
                "first_name": "Brian",
                "last_name": "Kalu",
                "role": "GUEST"
            }
        ]

        User.objects.all().delete()

        for user in users_data:
            print(f"seeding", user)
            user_obj= User.objects.create_user(id=uuid.uuid4(), **user)
            print("True")


        conversation_names = [
                "Weekend Plans",
                "Work Team Chat",
                "Family Group",
                "ALX Python Project",
                "Gaming Squad",
                "Fitness Buddies",
                "Book Club",
                "Startup Founders",
                "Study Group",
                "Movie Nights"
            ]
        users = User.objects.all()
        Conversation.objects.all().delete()
        for name in conversation_names:
            Conversation.objects.create(
                conversation_id=uuid.uuid4(),
                name=name,
                user=random.choice(users)
            )
            print("True")

        print("data seeded successfully")

