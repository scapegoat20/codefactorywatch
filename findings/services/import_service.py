"""CSV import with row-by-row validation (FR3, NFR7). Untrusted input: never crash."""
import csv
import io
from datetime import date

from findings.models import SEVERITIES, STATUSES, Finding, Technique

REQUIRED = ["title", "pillar", "technique_code", "severity", "status", "date_found", "description"]
MAX_BYTES = 1_000_000
MAX_ROWS = 5000


def parse_csv(uploaded):
    """Return (valid_rows, errors). valid_rows hold cleaned values; nothing is saved here."""
    errors, rows = [], []
    if uploaded.size > MAX_BYTES:
        return [], ["File: too large (limit 1 MB)."]
    if not uploaded.name.lower().endswith(".csv"):
        return [], ["File: must be a .csv file."]
    try:
        text = uploaded.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        return [], ["File: not valid UTF-8 text."]

    reader = csv.DictReader(io.StringIO(text))
    missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
    if missing:
        return [], ["File: missing column(s): " + ", ".join(missing)]

    techniques = {t.code: t for t in Technique.objects.select_related("pillar")}
    try:
        for n, raw in enumerate(reader, start=2):
            if n - 1 > MAX_ROWS:
                errors.append(f"File: only the first {MAX_ROWS} rows are processed.")
                break
            row = {k: (v or "").strip() for k, v in raw.items() if k}
            title = row["title"]
            tech = techniques.get(row["technique_code"])
            severity, status = row["severity"].title(), row["status"].title()
            problem = None
            if not title or len(title) > 200:
                problem = "title is required (max 200 characters)"
            elif tech is None:
                problem = f"unknown technique_code '{row['technique_code'][:20]}'"
            elif row["pillar"] and row["pillar"].lower() != tech.pillar.name.lower():
                problem = f"pillar does not match technique (expected {tech.pillar.name})"
            elif severity not in SEVERITIES:
                problem = "severity must be Low, Medium, High or Critical"
            elif status not in STATUSES:
                problem = "status must be Open, In Progress, Resolved or Closed"
            else:
                try:
                    found = date.fromisoformat(row["date_found"])
                except ValueError:
                    problem = "date_found must be YYYY-MM-DD"
            if problem:
                errors.append(f"Row {n}: {problem}.")
            else:
                rows.append({"title": title, "description": row["description"], "technique": tech,
                             "severity": severity, "status": status, "date_found": found})
    except csv.Error as exc:
        errors.append(f"File: could not be read as CSV ({exc}).")
    return rows, errors


def save_rows(rows, user):
    Finding.objects.bulk_create([Finding(reported_by=user, **r) for r in rows])
    return len(rows)
