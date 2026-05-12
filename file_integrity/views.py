"""Views for File Integrity Checker."""
import hashlib
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import FileCheck


def compute_sha256(file_obj) -> str:
    """Compute SHA-256 hash of uploaded file in chunks (memory efficient)."""
    sha256 = hashlib.sha256()
    for chunk in file_obj.chunks(chunk_size=8192):
        sha256.update(chunk)
    return sha256.hexdigest()


def checker_view(request):
    """Main file integrity checker page."""
    recent_checks = []
    if request.user.is_authenticated:
        recent_checks = FileCheck.objects.filter(user=request.user)[:10]
    return render(request, 'file_integrity/checker.html', {'recent_checks': recent_checks})


@require_http_methods(["POST"])
def check_file(request):
    """Handle file upload and hash computation."""
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    uploaded_file = request.FILES['file']
    expected_hash = request.POST.get('expected_hash', '').strip().lower()

    # Validate file size (10MB limit)
    if uploaded_file.size > 10 * 1024 * 1024:
        return JsonResponse({'error': 'File too large (max 10MB)'}, status=400)

    # Compute hash
    computed_hash = compute_sha256(uploaded_file)

    # Compare if expected hash provided
    integrity_ok = None
    match_result = None
    if expected_hash:
        # Validate hash format (64 hex chars for SHA-256)
        if len(expected_hash) != 64 or not all(c in '0123456789abcdef' for c in expected_hash):
            return JsonResponse({'error': 'Invalid SHA-256 hash format (must be 64 hex characters)'}, status=400)
        integrity_ok = computed_hash == expected_hash
        match_result = 'match' if integrity_ok else 'mismatch'

    # Save record
    check = FileCheck.objects.create(
        user=request.user if request.user.is_authenticated else None,
        filename=uploaded_file.name,
        file_size=uploaded_file.size,
        sha256_hash=computed_hash,
        expected_hash=expected_hash,
        integrity_ok=integrity_ok,
    )

    return JsonResponse({
        'filename': uploaded_file.name,
        'size': uploaded_file.size,
        'size_human': _human_size(uploaded_file.size),
        'sha256': computed_hash,
        'expected_hash': expected_hash,
        'match_result': match_result,
        'integrity_ok': integrity_ok,
        'check_id': check.pk,
    })


def _human_size(size_bytes: int) -> str:
    """Convert bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
