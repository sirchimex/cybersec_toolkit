"""Views for Encryption/Decryption Tool."""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from .utils import xor_encrypt, xor_decrypt, aes_encrypt, aes_decrypt
from .models import EncryptionLog


def tool_view(request):
    """Main encryption tool page."""
    return render(request, 'encryption_tool/tool.html')


@require_http_methods(["POST"])
def encrypt_view(request):
    """Handle encryption requests."""
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        key = data.get('key', '').strip()
        enc_type = data.get('type', 'aes')
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if not text:
        return JsonResponse({'error': 'Text cannot be empty'}, status=400)
    if not key:
        return JsonResponse({'error': 'Key/password cannot be empty'}, status=400)
    if len(text) > 10000:
        return JsonResponse({'error': 'Text too long (max 10,000 characters)'}, status=400)

    try:
        if enc_type == 'xor':
            result = xor_encrypt(text, key)
        elif enc_type == 'aes':
            result = aes_encrypt(text, key)
        else:
            return JsonResponse({'error': 'Unknown encryption type'}, status=400)

        # Log operation
        if request.user.is_authenticated:
            EncryptionLog.objects.create(user=request.user, operation='encrypt', encryption_type=enc_type)

        return JsonResponse({'result': result, 'type': enc_type})
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["POST"])
def decrypt_view(request):
    """Handle decryption requests."""
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        key = data.get('key', '').strip()
        enc_type = data.get('type', 'aes')
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if not text:
        return JsonResponse({'error': 'Ciphertext cannot be empty'}, status=400)
    if not key:
        return JsonResponse({'error': 'Key/password cannot be empty'}, status=400)

    try:
        if enc_type == 'xor':
            result = xor_decrypt(text, key)
        elif enc_type == 'aes':
            result = aes_decrypt(text, key)
        else:
            return JsonResponse({'error': 'Unknown encryption type'}, status=400)

        if request.user.is_authenticated:
            EncryptionLog.objects.create(user=request.user, operation='decrypt', encryption_type=enc_type)

        return JsonResponse({'result': result, 'type': enc_type})
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
