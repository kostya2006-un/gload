from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Genre,Album
User = get_user_model()


class MyApiTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com', password='password0123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        """База для Жанров"""
        Genre.objects.create(name='Rock')
        Genre.objects.create(name='Pop')
        """База для альбомов"""
        Album.objects.create(user = self.user, name = 'test_album1', description = 'des1')
        Album.objects.create(user = self.user, name = 'test_album2', description = 'des2')

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

    def test_public_albums_api(self):
        url = reverse('albums_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for album_data in response.data:
            name = album_data['name']
            description = album_data['description']
            user = album_data['user']
            cover = ''
            private = album_data['private']
            self.assertTrue(Album.objects.filter(name=name, description=description, user=user, cover=cover, private=private).exists())

    def test_author_albums_api(self):
        album_pk = 1
        url = reverse('albums_author', kwargs={'pk': album_pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Album.objects.count(),len(response.data))
        url2 = reverse('albums_author', kwargs={'pk':album_pk+1})
        response2 = self.client.get(url2)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(0, len(response2.data))

