from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Genre
User = get_user_model()


class MyApiTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com', password='password0123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        """База для Жанров"""
        Genre.objects.create(name='Rock')
        Genre.objects.create(name='Pop')

    def test_profile_api(self):
        url = reverse('profile_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        url = reverse('profile_api')
        data = {
            'first_name': 'New First Name',
            'last_name': 'New Last Name',

        }
        response = self.client.patch(url,data=data,format = 'multipart')
        self.assertEqual(response.status_code, 200)
        updated_profile = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_profile.first_name, 'New First Name')
        self.assertEqual(updated_profile.last_name, 'New Last Name')

    def test_genres_api(self):
        url = reverse('genres_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertIn({'name': 'Rock'}, response.data)
        self.assertIn({'name': 'Pop'}, response.data)