# CyberSec Toolkit 🔐

A Django-based cybersecurity education platform with four interactive tools.

## Features

| Tool | Description |
|------|-------------|
| 🔑 Password Checker | Real-time password strength analysis with scoring |
| 🔐 Encryption Tool | XOR and AES-256-CBC encrypt/decrypt |
| 🎣 Phishing Simulator | Click-to-identify phishing awareness training |
| 🔍 File Integrity | SHA-256 hash generation and verification |

---

## Quick Start

### 1. Install dependencies
```bash
pip install django pycryptodome
```

### 2. Run migrations
```bash
python manage.py migrate
```

### 3. Seed phishing scenarios
```bash
python manage.py seed_phishing
```

### 4. Create admin user (optional)
```bash
python manage.py createsuperuser
```

### 5. Start the server
```bash
python manage.py runserver
```

Open http://127.0.0.1:8000

**Demo admin:** username `admin` / password `admin123`

---

## Project Structure

```
cybersec_toolkit/       # Django project settings & main URLs
password_checker/       # App: password strength analysis
  views.py              # analyze_password() logic + AJAX endpoint
  models.py             # PasswordCheck model (stores metadata, NOT passwords)
encryption_tool/        # App: XOR and AES encryption
  utils.py              # xor_encrypt/decrypt, aes_encrypt/decrypt
  views.py              # encrypt/decrypt API endpoints
phishing_sim/           # App: phishing awareness simulator
  models.py             # PhishingScenario, PhishingIndicator, UserProgress
  management/commands/  # seed_phishing management command
file_integrity/         # App: file hash checker
  views.py              # SHA-256 computation and comparison
templates/              # All HTML templates (base + per-app)
```

---

## Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test password_checker
python manage.py test encryption_tool
python manage.py test file_integrity

# Verbose output
python manage.py test --verbosity=2
```

**24 tests across 4 apps** — all pass ✅

---

## Security Notes

- **CSRF protection** enabled on all POST endpoints
- **XOR cipher** is intentionally labeled as educational-only (not secure)
- **AES-256-CBC** uses random IV per encryption + SHA-256 key derivation
- **Passwords are never stored** — only metadata (length, criteria met)
- **File size limited** to 10MB for uploads
- Change `SECRET_KEY` in `settings.py` before production deployment
