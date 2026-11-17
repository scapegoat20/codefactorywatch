from django.conf import settings
from django.db import models

SEVERITIES = ["Low", "Medium", "High", "Critical"]
STATUSES = ["Open", "In Progress", "Resolved", "Closed"]
OPEN_STATUSES = ["Open", "In Progress"]
DONE_STATUSES = ["Resolved", "Closed"]


class Pillar(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Technique(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    pillar = models.ForeignKey(Pillar, on_delete=models.PROTECT, related_name="techniques")

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name} ({self.pillar})"


class Finding(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    technique = models.ForeignKey(Technique, on_delete=models.PROTECT, related_name="findings")
    severity = models.CharField(max_length=10, choices=[(s, s) for s in SEVERITIES], default="Medium")
    status = models.CharField(max_length=12, choices=[(s, s) for s in STATUSES], default="Open")
    date_found = models.DateField()
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                    on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_found", "-id"]

    def __str__(self):
        return self.title

    @property
    def pillar(self):
        return self.technique.pillar
