"""Management command to seed phishing scenarios into the database."""
from django.core.management.base import BaseCommand
from phishing_sim.models import PhishingScenario, PhishingIndicator


SCENARIOS = [
    {
        'title': 'Urgent Bank Alert',
        'scenario_type': 'email',
        'difficulty': 'easy',
        'order': 1,
        'content': '<div class="email-wrapper"><div class="email-header"><strong>From:</strong> <span id="sender">security@bankofamerica-alerts.net</span><br><strong>Subject:</strong> <span id="subject">URGENT: Account SUSPENDED in 24 hours!</span></div><div class="email-body"><p>Dear Valued Customer,</p><p id="urgency">Your account has been flagged. You MUST verify within <strong>24 HOURS</strong> or face permanent suspension!</p><p>Click here: <a href="#" id="fake-link">https://secure-bankofamerica-verify.com/login</a></p><p id="threat">Failure to act will result in permanent closure and legal action.</p><p>Bank of America Security Team</p></div></div>',
        'indicators': [
            {'element_id': 'sender', 'description': 'Suspicious lookalike sender domain', 'educational_tip': 'The sender domain is "bankofamerica-alerts.net" NOT "bankofamerica.com". Attackers register lookalike domains. Always check the full email domain carefully.'},
            {'element_id': 'subject', 'description': 'Urgent/threatening subject with ALL CAPS', 'educational_tip': 'Legitimate organizations rarely use ALL CAPS or excessive punctuation. Creating panic is a social engineering tactic to bypass rational thinking.'},
            {'element_id': 'fake-link', 'description': 'Misleading URL with fake domain', 'educational_tip': '"secure-bankofamerica-verify.com" is NOT the official bank site. Always hover over links before clicking. Real bank URL would be bankofamerica.com.'},
            {'element_id': 'threat', 'description': 'Threatening language and false urgency', 'educational_tip': 'Threatening "legal action" or "permanent suspension" is designed to frighten you into acting without thinking. Real banks never threaten via email without prior communication.'},
        ]
    },
    {
        'title': 'PayPal Password Reset',
        'scenario_type': 'email',
        'difficulty': 'medium',
        'order': 2,
        'content': '<div class="email-wrapper"><div class="email-header"><strong>From:</strong> <span id="sender">no-reply@paypa1.com</span><br><strong>Subject:</strong> Password Reset Request</div><div class="email-body"><p>Hi there,</p><p>We received a request to reset your PayPal password.</p><p id="button-area"><a href="#" id="reset-btn" style="background:#003087;color:white;padding:12px 24px;text-decoration:none;border-radius:4px;display:inline-block;">Reset My Password</a></p><p id="expiry">This link expires in <strong>10 minutes</strong>.</p><p id="disclaimer">If you did not request this, call us at <span id="fake-phone">1-800-555-PAYL</span></p><p>The PayPal Team</p></div></div>',
        'indicators': [
            {'element_id': 'sender', 'description': 'Domain uses number "1" instead of letter "l"', 'educational_tip': '"paypa1.com" uses numeral 1 instead of letter l. This typosquatting tactic is very common. Examine email domains character by character.'},
            {'element_id': 'expiry', 'description': 'Artificial extreme time pressure', 'educational_tip': 'Saying the link expires in 10 minutes creates pressure to act without verification. Real password resets typically last 24-48 hours.'},
            {'element_id': 'fake-phone', 'description': 'Non-standard customer service number', 'educational_tip': 'PayPal\'s real number is 1-888-221-1161. Always verify contact numbers from the official website, never from within a suspicious email.'},
        ]
    },
    {
        'title': 'IT Department Credential Harvest',
        'scenario_type': 'email',
        'difficulty': 'hard',
        'order': 3,
        'content': '<div class="email-wrapper"><div class="email-header"><strong>From:</strong> <span id="sender">it-support@yourcompany-helpdesk.com</span><br><strong>Subject:</strong> <span id="subject">Action Required: Microsoft 365 License Renewal</span></div><div class="email-body"><p>Dear Team Member,</p><p>Our Microsoft 365 licenses are being renewed. All employees must re-authenticate by <strong id="deadline">end of business TODAY</strong>.</p><p>Log in at: <a href="#" id="fake-link">https://login.microsoftonline.com.yourcompany-helpdesk.com/auth</a></p><p id="legit-look">Verify this request with IT at extension 4499.</p><p id="attachment">Review attached: <a href="#">Security_Policy_Update.pdf.exe</a></p><p>IT Support Helpdesk</p></div></div>',
        'indicators': [
            {'element_id': 'sender', 'description': 'External domain posing as internal IT', 'educational_tip': 'Internal IT uses internal company email domains. "yourcompany-helpdesk.com" is NOT "yourcompany.com". Any IT request should come from your actual company domain.'},
            {'element_id': 'fake-link', 'description': 'Subdomain trick on Microsoft URL', 'educational_tip': 'The URL uses "login.microsoftonline.com.yourcompany-helpdesk.com" — the REAL domain is "yourcompany-helpdesk.com". The domain is always what comes right before the first single slash.'},
            {'element_id': 'deadline', 'description': 'Same-day deadline pressure', 'educational_tip': 'Legitimate IT renewals are planned in advance and never require end-of-day action. Same-day deadlines prevent you from verifying the request.'},
            {'element_id': 'attachment', 'description': 'Double extension executable disguised as PDF', 'educational_tip': '"Security_Policy_Update.pdf.exe" — the .exe is the real file type. Windows hides known extensions by default. NEVER run .exe files from emails.'},
        ]
    },
]


class Command(BaseCommand):
    help = 'Seed phishing simulation scenarios'

    def handle(self, *args, **options):
        PhishingIndicator.objects.all().delete()
        PhishingScenario.objects.all().delete()
        for s_data in SCENARIOS:
            indicators = s_data.pop('indicators')
            scenario = PhishingScenario.objects.create(**s_data)
            for ind in indicators:
                PhishingIndicator.objects.create(scenario=scenario, **ind)
            self.stdout.write(f"Created: {scenario.title}")
        self.stdout.write(self.style.SUCCESS('Phishing scenarios seeded!'))
