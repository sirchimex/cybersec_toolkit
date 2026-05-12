"""Tests for Password Checker app."""
from django.test import TestCase, Client
from django.urls import reverse
import json
from .views import analyze_password


class PasswordAnalysisTests(TestCase):
    def test_weak_password(self):
        result = analyze_password("abc")
        self.assertLess(result['score'], 30)
        self.assertEqual(result['label'], 'Very Weak')

    def test_strong_password(self):
        result = analyze_password("MyStr0ng!P@ssw0rd#2024")
        self.assertGreaterEqual(result['score'], 70)

    def test_common_password_detected(self):
        result = analyze_password("password")
        self.assertFalse(result['criteria']['not_common'])

    def test_uppercase_detected(self):
        result = analyze_password("Hello")
        self.assertTrue(result['criteria']['has_uppercase'])

    def test_symbols_detected(self):
        result = analyze_password("test!@#")
        self.assertTrue(result['criteria']['has_symbols'])

    def test_sequential_detected(self):
        result = analyze_password("abc123")
        self.assertFalse(result['criteria']['no_sequential'])


class PasswordCheckerViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_checker_page_loads(self):
        response = self.client.get('/password/')
        self.assertEqual(response.status_code, 200)

    def test_ajax_endpoint(self):
        response = self.client.post('/password/check/',
            data=json.dumps({'password': 'TestPassword123!'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('score', data)
        self.assertIn('label', data)

    def test_empty_password(self):
        response = self.client.post('/password/check/',
            data=json.dumps({'password': ''}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['score'], 0)
