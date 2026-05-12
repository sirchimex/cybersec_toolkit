"""Tests for File Integrity Checker."""
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
import hashlib


class FileIntegrityTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_checker_page_loads(self):
        response = self.client.get('/integrity/')
        self.assertEqual(response.status_code, 200)

    def test_file_hash_computed_correctly(self):
        content = b"Test file content for hashing"
        expected_hash = hashlib.sha256(content).hexdigest()
        f = SimpleUploadedFile("test.txt", content, content_type="text/plain")
        response = self.client.post('/integrity/check/', {'file': f})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['sha256'], expected_hash)

    def test_matching_hash_detected(self):
        content = b"File to verify"
        correct_hash = hashlib.sha256(content).hexdigest()
        f = SimpleUploadedFile("verify.txt", content)
        response = self.client.post('/integrity/check/', {'file': f, 'expected_hash': correct_hash})
        data = response.json()
        self.assertTrue(data['integrity_ok'])
        self.assertEqual(data['match_result'], 'match')

    def test_mismatching_hash_detected(self):
        content = b"Original content"
        wrong_hash = hashlib.sha256(b"Different content").hexdigest()
        f = SimpleUploadedFile("tampered.txt", content)
        response = self.client.post('/integrity/check/', {'file': f, 'expected_hash': wrong_hash})
        data = response.json()
        self.assertFalse(data['integrity_ok'])
        self.assertEqual(data['match_result'], 'mismatch')

    def test_invalid_hash_format(self):
        f = SimpleUploadedFile("test.txt", b"data")
        response = self.client.post('/integrity/check/', {'file': f, 'expected_hash': 'not-a-valid-hash'})
        self.assertEqual(response.status_code, 400)
