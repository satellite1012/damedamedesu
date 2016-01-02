import unittest
from django.test import TestCase, Client
from django.contrib.auth.models import User

class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'homura'
        self.password = 'test'
        self.test_user = User.objects.create_user(username=self.username, password=self.password)
        login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(login, True)
        
    def tearDown(self):
        self.test_user.delete()
        
    def test_mainpage(self):
        response = self.client.get('/portal/')
        self.assertEqual(response.status_code, 200)
    
    def test_mysongs(self):
        response = self.client.get('/portal/mysongs/')
        self.assertEqual(response.status_code, 200)
    
    def test_ratehistory(self):
        response = self.client.get('/portal/history/rate/')
        self.assertEqual(response.status_code, 200)
    
    def test_gifthistory(self):
        response = self.client.get('/portal/history/gift/')
        self.assertEqual(response.status_code, 200)
    
    