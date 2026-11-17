# CodeFactory Watch (MVP)

A Django dashboard that records SDLC security findings, maps them to the five SITF pillars and
shows Matplotlib charts. Built for BCS 3106.

## Run locally

```
python -m venv venv
venv\Scripts\activate            (Windows)     source venv/bin/activate   (Linux/macOS)
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo       # pillars, example techniques, Analyst/Viewer groups, demo findings
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and log in.

## Roles
- **Superuser**: everything, plus /admin/ for users and the technique catalogue.
- **Analyst** group: add, edit, close findings and import CSV.
- **Viewer** group: read-only (dashboard, list, export).
Create users in /admin/ and add them to a group.

## CSV import
Use `sample_findings.csv` as a template.

## Tests (used by CI/CD in Part 2)
```
python manage.py test
```
Test names carry the Requirements Traceability Matrix IDs (TC-01 ... TC-16).

## Secure coding in this MVP
CSRF tokens on all forms, template auto-escaping, ORM only (no raw SQL), hashed passwords,
login and permission checks on every view, CSV validation with size/type limits, CSV-formula
protection on export, secrets from environment variables (`DJANGO_SECRET_KEY`), HTTPS settings
when `DJANGO_DEBUG=0`.

## Not in the MVP yet
Remediation tasks (FR5), PDF export (FR6), audit log (FR8). Add them as the next iterations.
