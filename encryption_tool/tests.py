"""Tests for Encryption Tool app."""
from django.test import TestCase, Client
import json
from .utils import xor_encrypt, xor_decrypt, aes_encrypt, aes_decrypt


class XORTests(TestCase):
    def test_encrypt_decrypt_roundtrip(self):
        original = "Hello, World!"
        key = "secret"
        encrypted = xor_encrypt(original, key)
        decrypted = xor_decrypt(encrypted, key)
        self.assertEqual(decrypted, original)

    def test_different_keys_give_different_output(self):
        text = "test message"
        self.assertNotEqual(xor_encrypt(text, "key1"), xor_encrypt(text, "key2"))

    def test_empty_key_raises(self):
        with self.assertRaises(ValueError):
            xor_encrypt("text", "")


class AESTests(TestCase):
    def test_encrypt_decrypt_roundtrip(self):
        original = "Secret message for AES test"
        password = "mypassword123"
        encrypted = aes_encrypt(original, password)
        decrypted = aes_decrypt(encrypted, password)
        self.assertEqual(decrypted, original)

    def test_wrong_key_fails(self):
        encrypted = aes_encrypt("test", "correct_key")
        with self.assertRaises(ValueError):
            aes_decrypt(encrypted, "wrong_key")

    def test_random_iv_gives_different_output(self):
        text, key = "same text", "same key"
        self.assertNotEqual(aes_encrypt(text, key), aes_encrypt(text, key))

    def test_unicode_support(self):
        original = "Unicode: 中文 العربية 日本語"
        password = "unicode_test"
        self.assertEqual(aes_decrypt(aes_encrypt(original, password), password), original)


class EncryptionViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_tool_page_loads(self):
        response = self.client.get('/encryption/')
        self.assertEqual(response.status_code, 200)

    def test_encrypt_endpoint(self):
        response = self.client.post('/encryption/encrypt/',
            data=json.dumps({'text': 'Hello', 'key': 'testkey', 'type': 'aes'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('result', data)

    def test_decrypt_endpoint(self):
        # First encrypt
        enc_res = self.client.post('/encryption/encrypt/',
            data=json.dumps({'text': 'Hello World', 'key': 'mykey', 'type': 'aes'}),
            content_type='application/json')
        enc_data = json.loads(enc_res.content)
        # Then decrypt
        dec_res = self.client.post('/encryption/decrypt/',
            data=json.dumps({'text': enc_data['result'], 'key': 'mykey', 'type': 'aes'}),
            content_type='application/json')
        dec_data = json.loads(dec_res.content)
        self.assertEqual(dec_data['result'], 'Hello World')
