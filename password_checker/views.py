"""Views for Password Strength Checker."""
import re
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import PasswordCheck

# Common weak passwords to flag
COMMON_PASSWORDS = {
    'password', '123456', 'password1', 'qwerty', 'abc123',
    'letmein', 'monkey', 'master', 'dragon', 'iloveyou',
    '1234567890', 'admin', 'welcome', 'login', 'pass',
}


def analyze_password(password: str) -> dict:
    """
    Analyze password strength and return detailed feedback.
    Returns a dict with score, label, criteria met, and suggestions.
    """
    score = 0
    suggestions = []
    criteria = {
        'length_ok': len(password) >= 8,
        'length_good': len(password) >= 12,
        'length_great': len(password) >= 16,
        'has_uppercase': bool(re.search(r'[A-Z]', password)),
        'has_lowercase': bool(re.search(r'[a-z]', password)),
        'has_digits': bool(re.search(r'\d', password)),
        'has_symbols': bool(re.search(r'[!@#$%^&*(),.?":{}|<>_\-\[\]\\;\'`~/+=]', password)),
        'no_spaces': ' ' not in password,
        'not_common': password.lower() not in COMMON_PASSWORDS,
        'no_repeats': not bool(re.search(r'(.)\1{2,}', password)),  # no 3+ repeated chars
        'no_sequential': not bool(re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def)', password.lower())),
    }

    # Score calculation
    if criteria['length_ok']:
        score += 15
    if criteria['length_good']:
        score += 10
    if criteria['length_great']:
        score += 10
    if criteria['has_uppercase']:
        score += 10
    if criteria['has_lowercase']:
        score += 10
    if criteria['has_digits']:
        score += 10
    if criteria['has_symbols']:
        score += 15
    if criteria['not_common']:
        score += 10
    if criteria['no_repeats']:
        score += 5
    if criteria['no_sequential']:
        score += 5

    # Suggestions
    if not criteria['length_ok']:
        suggestions.append("Use at least 8 characters")
    elif not criteria['length_good']:
        suggestions.append("Increase length to 12+ characters for better security")
    elif not criteria['length_great']:
        suggestions.append("Consider 16+ characters for maximum security")
    if not criteria['has_uppercase']:
        suggestions.append("Add uppercase letters (A-Z)")
    if not criteria['has_lowercase']:
        suggestions.append("Add lowercase letters (a-z)")
    if not criteria['has_digits']:
        suggestions.append("Include numbers (0-9)")
    if not criteria['has_symbols']:
        suggestions.append("Add special characters (!@#$%^&*)")
    if not criteria['not_common']:
        suggestions.append("Avoid commonly used passwords")
    if not criteria['no_repeats']:
        suggestions.append("Avoid repeating the same character multiple times")
    if not criteria['no_sequential']:
        suggestions.append("Avoid sequential patterns like '123' or 'abc'")

    # Label
    if score < 30:
        label = 'Very Weak'
        color = 'danger'
    elif score < 50:
        label = 'Weak'
        color = 'warning'
    elif score < 70:
        label = 'Fair'
        color = 'info'
    elif score < 85:
        label = 'Strong'
        color = 'success'
    else:
        label = 'Very Strong'
        color = 'success'

    return {
        'score': score,
        'label': label,
        'color': color,
        'criteria': criteria,
        'suggestions': suggestions,
        'length': len(password),
    }


def checker_view(request):
    """Main password checker page."""
    return render(request, 'password_checker/checker.html')


@require_http_methods(["POST"])
def check_password_ajax(request):
    """AJAX endpoint: analyze password strength in real-time."""
    try:
        data = json.loads(request.body)
        password = data.get('password', '')
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if not password:
        return JsonResponse({'score': 0, 'label': 'Empty', 'color': 'secondary',
                             'criteria': {}, 'suggestions': [], 'length': 0})

    result = analyze_password(password)

    # Optionally save check for logged-in users (without storing the actual password)
    if request.user.is_authenticated:
        PasswordCheck.objects.create(
            user=request.user,
            strength_score=result['score'],
            strength_label=result['label'],
            length=result['length'],
            has_uppercase=result['criteria']['has_uppercase'],
            has_lowercase=result['criteria']['has_lowercase'],
            has_digits=result['criteria']['has_digits'],
            has_symbols=result['criteria']['has_symbols'],
        )

    return JsonResponse(result)
