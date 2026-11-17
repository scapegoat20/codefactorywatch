from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("findings/", views.finding_list, name="finding_list"),
    path("findings/new/", views.finding_add, name="finding_add"),
    path("findings/<int:pk>/edit/", views.finding_edit, name="finding_edit"),
    path("findings/<int:pk>/close/", views.finding_close, name="finding_close"),
    path("import/", views.import_csv, name="import_csv"),
    path("export/", views.export_csv, name="export_csv"),
]
