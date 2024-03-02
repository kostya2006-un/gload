from django.urls import reverse
from rest_framework.test import APITestCase
from django.core import mail
import re


class AuthTests(APITestCase):

    def setUp(self):
        super().setUp()
        url = reverse('customuser-list')
        response = self.client.post(url, {'email': 'test@example.com', 'password': 'password0123'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, ['test@example.com'])

        email_body = email.body
        url_pattern = re.compile(r'http://testserver/activate/\w+/\w+-\w+')

        # Поиск URL в тексте письма
        match = url_pattern.search(email_body)

        activation_url = match.group()

        activation_url = activation_url[27:]

        uid = activation_url[0:2]
        token = activation_url[3:]

        self.uid = uid
        self.token = token

    def test_activation(self):
        url = reverse('customuser-activation')
        response = self.client.post(url,{'uid':self.uid,'token': self.token}, format = 'json')
        self.assertEqual(response.status_code,204)
