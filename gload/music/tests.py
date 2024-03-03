from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.urls import reverse

class MyApiTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com', password='password0123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_profile_api(self):
        url = reverse('profile_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
