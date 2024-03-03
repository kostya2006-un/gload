from django.urls import reverse
from rest_framework.test import APITestCase
from django.core import mail
import re


class AuthTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.user_email = 'test@example.com'
        self.user_password = 'password0123'
        self.invalid_email = 'test@examplsde.com'

    def register_user(self):
        url = reverse('customuser-list')
        response = self.client.post(url, {'email': self.user_email, 'password': self.user_password}, format='json')
        return response

    def get_activation_details(self, email_body):
        url_pattern = re.compile(r'http://testserver/activate/\w+/\w+-\w+')
        match = url_pattern.search(email_body)
        activation_url = match.group()
        activation_url = activation_url[27:]
        uid = activation_url[0:2]
        token = activation_url[3:]
        return uid, token

    def activate(self):
        url = reverse('customuser-activation')
        res = self.register_user()
        email = mail.outbox[0]
        uid,token = self.get_activation_details(email.body)
        response = self.client.post(url, {'uid': uid, 'token': token}, format='json')
        return response

    def test_user_registration(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, [self.user_email])
        uid, token = self.get_activation_details(email.body)
        self.assertIsNotNone(uid)
        self.assertIsNotNone(token)

    def test_activation(self):
        self.register_user()
        email_body = mail.outbox[0].body
        uid, token = self.get_activation_details(email_body)
        url = reverse('customuser-activation')
        response = self.client.post(url, {'uid': uid, 'token': token}, format='json')
        self.assertEqual(response.status_code, 204)

    def test_login(self):
        self.register_user()
        self.activate()
        url = reverse('login')
        response1 = self.client.post(url, {'email': self.user_email, 'password': self.user_password}, format='json')
        response2 = self.client.post(url, {'email': self.invalid_email, 'password': self.user_password}, format='json')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 400)




