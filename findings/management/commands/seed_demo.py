"""python manage.py seed_demo  -> pillars, example techniques, role groups and demo findings."""
import random
from datetime import date, timedelta

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from findings.models import Finding, Pillar, Technique

# Illustrative techniques. Replace codes/names with the real SITF catalogue entries.
TECHNIQUES = {
    "Endpoint/IDE": [("IDE-01", "Malicious IDE extension"), ("IDE-02", "Developer workstation compromise")],
    "VCS": [("VCS-01", "Imposter Commits"), ("VCS-02", "Secrets leaked in repository")],
    "CI/CD": [("CICD-01", "Action Cache Poisoning"), ("CICD-02", "Compromised build runner")],
    "Registry": [("REG-01", "Dependency confusion"), ("REG-02", "Malicious package publish")],
    "Production": [("PRD-01", "Stolen deployment credentials")],
}


class Command(BaseCommand):
    help = "Create pillars, example techniques, Analyst/Viewer groups and demo findings."

    def handle(self, *args, **options):
        for pname, techs in TECHNIQUES.items():
            pillar, _ = Pillar.objects.get_or_create(name=pname)
            for code, name in techs:
                Technique.objects.get_or_create(code=code, defaults={"name": name, "pillar": pillar})

        view = Permission.objects.get(codename="view_finding")
        analyst, _ = Group.objects.get_or_create(name="Analyst")
        analyst.permissions.set(Permission.objects.filter(
            codename__in=["view_finding", "add_finding", "change_finding"]))
        viewer, _ = Group.objects.get_or_create(name="Viewer")
        viewer.permissions.set([view])

        if not Finding.objects.exists():
            rnd, techs, today = random.Random(7), list(Technique.objects.all()), date.today()
            sev = ["Low", "Medium", "High", "Critical"]
            stat = ["Open", "In Progress", "Resolved", "Closed"]
            for i in range(24):
                t = rnd.choice(techs)
                Finding.objects.create(
                    title=f"Demo finding {i + 1}: {t.name}", technique=t,
                    description="Sample data for the demo dashboard.",
                    severity=rnd.choice(sev), status=rnd.choice(stat),
                    date_found=today - timedelta(days=rnd.randint(0, 150)))
        self.stdout.write(self.style.SUCCESS("Seed data ready."))
