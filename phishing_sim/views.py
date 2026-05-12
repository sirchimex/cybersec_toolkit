"""Views for Phishing Awareness Simulator."""
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import PhishingScenario, PhishingIndicator, UserProgress


def simulator_home(request):
    """List all phishing scenarios."""
    scenarios = PhishingScenario.objects.all()
    progress_map = {}
    if request.user.is_authenticated:
        for p in UserProgress.objects.filter(user=request.user):
            progress_map[p.scenario_id] = p.score_percent
    return render(request, 'phishing_sim/home.html', {
        'scenarios': scenarios,
        'progress_map': progress_map,
    })


def scenario_view(request, pk):
    """Display a single phishing scenario for analysis."""
    scenario = get_object_or_404(PhishingScenario, pk=pk)
    total = scenario.indicators.count()
    return render(request, 'phishing_sim/scenario.html', {
        'scenario': scenario,
        'total_indicators': total,
    })


@require_http_methods(["POST"])
def submit_answers(request, pk):
    """Process user's submitted answers for a scenario."""
    scenario = get_object_or_404(PhishingScenario, pk=pk)
    try:
        data = json.loads(request.body)
        found_ids = set(data.get('found', []))
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    all_indicators = list(scenario.indicators.all())
    correct_ids = {ind.element_id for ind in all_indicators}
    found_correct = found_ids & correct_ids
    missed = correct_ids - found_ids
    false_positives = found_ids - correct_ids

    score = len(found_correct) / len(correct_ids) * 100 if correct_ids else 0

    # Save progress for authenticated users
    if request.user.is_authenticated:
        UserProgress.objects.create(
            user=request.user,
            scenario=scenario,
            indicators_found=len(found_correct),
            total_indicators=len(correct_ids),
            score_percent=score,
        )

    # Build detailed feedback
    feedback = []
    for ind in all_indicators:
        feedback.append({
            'element_id': ind.element_id,
            'description': ind.description,
            'tip': ind.educational_tip,
            'found': ind.element_id in found_correct,
        })

    return JsonResponse({
        'score': round(score, 1),
        'found_correct': len(found_correct),
        'total': len(correct_ids),
        'false_positives': len(false_positives),
        'feedback': feedback,
    })


@login_required
def progress_view(request):
    """Show user's phishing awareness progress."""
    attempts = UserProgress.objects.filter(user=request.user).select_related('scenario')[:20]
    scenarios = PhishingScenario.objects.all()
    stats = {}
    for s in scenarios:
        user_attempts = [a for a in attempts if a.scenario_id == s.pk]
        if user_attempts:
            avg = sum(a.score_percent for a in user_attempts) / len(user_attempts)
            best = max(a.score_percent for a in user_attempts)
            stats[s.pk] = {'avg': round(avg, 1), 'best': round(best, 1), 'count': len(user_attempts)}
    return render(request, 'phishing_sim/progress.html', {
        'attempts': attempts, 'stats': stats, 'scenarios': scenarios
    })
