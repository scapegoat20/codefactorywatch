"""Dashboard data and Matplotlib charts (FR4). Figure() is used so no GUI backend is needed."""
import base64
from io import BytesIO

from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from matplotlib.figure import Figure

from findings.models import DONE_STATUSES, OPEN_STATUSES, SEVERITIES, Finding, Pillar

SEV_COLORS = {"Low": "#7fb069", "Medium": "#f2c14e", "High": "#f08a4b", "Critical": "#d1495b"}


def _encode(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    return base64.b64encode(buf.getvalue()).decode("ascii")


def _empty(ax):
    ax.text(0.5, 0.5, "No data yet", ha="center", va="center", transform=ax.transAxes)
    ax.set_xticks([])
    ax.set_yticks([])


def chart_by_pillar():
    data = Pillar.objects.annotate(n=Count("techniques__findings")).order_by("id")
    names, counts = [p.name for p in data], [p.n for p in data]
    fig = Figure(figsize=(5.4, 3.4))
    ax = fig.subplots()
    ax.bar(names, counts, color="#3d5a80")
    ax.set_title("Findings per SITF pillar")
    ax.set_ylabel("Findings")
    ax.tick_params(axis="x", labelrotation=20)
    ax.yaxis.get_major_locator().set_params(integer=True)
    for i, c in enumerate(counts):
        ax.text(i, c, str(c), ha="center", va="bottom", fontsize=9)
    return _encode(fig)


def chart_severity():
    counts = {s: 0 for s in SEVERITIES}
    for row in Finding.objects.values("severity").annotate(n=Count("id")):
        counts[row["severity"]] = row["n"]
    fig = Figure(figsize=(5.4, 3.4))
    ax = fig.subplots()
    if sum(counts.values()) == 0:
        _empty(ax)
    else:
        ax.bar(counts.keys(), counts.values(), color=[SEV_COLORS[s] for s in counts])
        ax.yaxis.get_major_locator().set_params(integer=True)
        ax.set_ylabel("Findings")
    ax.set_title("Severity distribution")
    return _encode(fig)


def chart_trend():
    rows = (Finding.objects.annotate(m=TruncMonth("date_found")).values("m")
            .annotate(open=Count("id", filter=Q(status__in=OPEN_STATUSES)),
                      done=Count("id", filter=Q(status__in=DONE_STATUSES))).order_by("m"))
    months = [r["m"].strftime("%b %Y") for r in rows]
    fig = Figure(figsize=(10.8, 3.2))
    ax = fig.subplots()
    if not months:
        _empty(ax)
    else:
        ax.plot(months, [r["open"] for r in rows], marker="o", color="#d1495b", label="Open / in progress")
        ax.plot(months, [r["done"] for r in rows], marker="o", color="#2a9d8f", label="Resolved / closed")
        ax.yaxis.get_major_locator().set_params(integer=True)
        ax.set_ylabel("Findings found")
        ax.legend()
    ax.set_title("Open versus resolved, by month found")
    return _encode(fig)


def build_dashboard():
    qs = Finding.objects
    return {
        "total": qs.count(),
        "open": qs.filter(status__in=OPEN_STATUSES).count(),
        "critical_open": qs.filter(status__in=OPEN_STATUSES, severity="Critical").count(),
        "resolved": qs.filter(status__in=DONE_STATUSES).count(),
        "pillar_chart": chart_by_pillar(),
        "severity_chart": chart_severity(),
        "trend_chart": chart_trend(),
    }
