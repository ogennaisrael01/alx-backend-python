from django.test import TestCase, Client
from rest_framework import status
import time
from faker import Faker
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied

User = get_user_model()


class MiddlewareTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.endpoint = "/api/v1/conversations/" 
        self.faker = Faker()
        self.user = User.objects.create_superuser(
            username="ogenna", 
            email="movins806@gmail.com", 
            password="", 
            )

    def test_restrict_access_middleware(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_max_rate_limiting_middleware(self):
        self.client.force_login(self.user)
        data = {
            "name": self.faker.sentence()[:20],
            "description": self.faker.sentences()
        }
        # make request to exceed maximum allowed messages
        for _ in range(10):
            response = self.client.post(self.endpoint, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
