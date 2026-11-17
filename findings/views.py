import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CSVUploadForm, FindingForm
from .models import SEVERITIES, STATUSES, Finding, Pillar
from .services import import_service
from .services.charts import build_dashboard


@login_required
def dashboard(request):
    return render(request, "findings/dashboard.html", build_dashboard())


@login_required
def finding_list(request):
    qs = Finding.objects.select_related("technique__pillar")
    pillar, severity, status = (request.GET.get(k, "") for k in ("pillar", "severity", "status"))
    pillars = list(Pillar.objects.values_list("name", flat=True))
    if pillar in pillars:
        qs = qs.filter(technique__pillar__name=pillar)
    if severity in SEVERITIES:
        qs = qs.filter(severity=severity)
    if status in STATUSES:
        qs = qs.filter(status=status)
    return render(request, "findings/finding_list.html", {
        "findings": qs, "pillars": pillars, "severities": SEVERITIES, "statuses": STATUSES,
        "sel": {"pillar": pillar, "severity": severity, "status": status}})


@permission_required("findings.add_finding", raise_exception=True)
def finding_add(request):
    form = FindingForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        finding = form.save(commit=False)
        finding.reported_by = request.user
        finding.save()
        messages.success(request, "Finding saved.")
        return redirect("finding_list")
    return render(request, "findings/finding_form.html", {"form": form, "heading": "New finding"})


@permission_required("findings.change_finding", raise_exception=True)
def finding_edit(request, pk):
    finding = get_object_or_404(Finding, pk=pk)
    form = FindingForm(request.POST or None, instance=finding)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Finding updated.")
        return redirect("finding_list")
    return render(request, "findings/finding_form.html", {"form": form, "heading": "Edit finding"})


@permission_required("findings.change_finding", raise_exception=True)
@require_POST
def finding_close(request, pk):
    finding = get_object_or_404(Finding, pk=pk)
    finding.status = "Closed"
    finding.save(update_fields=["status"])
    messages.success(request, "Finding closed.")
    return redirect("finding_list")


@permission_required("findings.add_finding", raise_exception=True)
def import_csv(request):
    form, errors = CSVUploadForm(request.POST or None, request.FILES or None), []
    if request.method == "POST" and form.is_valid():
        rows, errors = import_service.parse_csv(form.cleaned_data["file"])
        if rows:
            count = import_service.save_rows(rows, request.user)
            messages.success(request, f"{count} finding(s) imported.")
        if not errors and rows:
            return redirect("finding_list")
        if not rows and not errors:
            errors = ["File: no data rows found."]
    return render(request, "findings/import.html", {"form": form, "errors": errors})


def _safe_cell(value):
    """Prevent spreadsheet formula injection in exported CSV."""
    text = str(value)
    return "'" + text if text[:1] in ("=", "+", "-", "@") else text


@login_required
def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="findings.csv"'
    writer = csv.writer(response)
    writer.writerow(import_service.REQUIRED)
    for f in Finding.objects.select_related("technique__pillar"):
        writer.writerow([_safe_cell(v) for v in (f.title, f.pillar.name, f.technique.code, f.severity,
                                                  f.status, f.date_found.isoformat(), f.description)])
    return response
