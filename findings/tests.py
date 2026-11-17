"""Unit tests. IDs match the Requirements Traceability Matrix (TC-xx)."""
from django.contrib.auth.models import Group, Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from findings.models import Finding, Pillar, Technique
from findings.services import import_service

HEADER = "title,pillar,technique_code,severity,status,date_found,description\n"


class BaseCase(TestCase):
    def setUp(self):
        pillar = Pillar.objects.create(name="CI/CD")
        self.tech = Technique.objects.create(code="CICD-01", name="Action Cache Poisoning", pillar=pillar)
        analyst = Group.objects.create(name="Analyst")
        analyst.permissions.set(Permission.objects.filter(
            codename__in=["view_finding", "add_finding", "change_finding"]))
        viewer = Group.objects.create(name="Viewer")
        viewer.permissions.set(Permission.objects.filter(codename="view_finding"))
        self.analyst = User.objects.create_user("ana", password="pw-Test-12345")
        self.analyst.groups.add(analyst)
        self.viewer = User.objects.create_user("vic", password="pw-Test-12345")
        self.viewer.groups.add(viewer)

    def data(self, **extra):
        d = {"title": "Cache poisoned", "description": "x", "technique": self.tech.pk,
             "severity": "High", "status": "Open", "date_found": "2026-10-01"}
        d.update(extra)
        return d


class FindingTests(BaseCase):
    def test_tc01_login_and_wrong_password(self):
        self.assertTrue(self.client.login(username="ana", password="pw-Test-12345"))
        self.client.logout()
        self.assertFalse(self.client.login(username="ana", password="wrong"))

    def test_tc02_viewer_cannot_create(self):
        self.client.force_login(self.viewer)
        response = self.client.post(reverse("finding_add"), self.data())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Finding.objects.count(), 0)

    def test_tc03_analyst_creates_finding(self):
        self.client.force_login(self.analyst)
        response = self.client.post(reverse("finding_add"), self.data())
        self.assertRedirects(response, reverse("finding_list"))
        self.assertEqual(Finding.objects.get().title, "Cache poisoned")

    def test_tc04_close_finding(self):
        self.client.force_login(self.analyst)
        f = Finding.objects.create(title="t", technique=self.tech, date_found="2026-10-01")
        self.client.post(reverse("finding_close", args=[f.pk]))
        f.refresh_from_db()
        self.assertEqual(f.status, "Closed")

    def test_tc07_dashboard_renders_charts(self):
        self.client.force_login(self.viewer)
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, "data:image/png;base64,", count=3)

    def test_tc10_csv_export(self):
        Finding.objects.create(title="=cmd()", technique=self.tech, date_found="2026-10-01")
        self.client.force_login(self.viewer)
        response = self.client.get(reverse("export_csv"))
        self.assertIn("'=cmd()", response.content.decode())

    def test_login_required(self):
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 302)


class ImportTests(BaseCase):
    def upload(self, content, name="f.csv"):
        return SimpleUploadedFile(name, content.encode(), content_type="text/csv")

    def test_tc05_valid_csv_imports(self):
        self.client.force_login(self.analyst)
        csv_text = HEADER + "Bad runner,CI/CD,CICD-01,High,Open,2026-10-02,desc\n"
        self.client.post(reverse("import_csv"), {"file": self.upload(csv_text)})
        self.assertEqual(Finding.objects.count(), 1)

    def test_tc06_malformed_csv_rejected(self):
        rows, errors = import_service.parse_csv(self.upload("not,a,valid,header\n1,2,3,4\n"))
        self.assertEqual(rows, [])
        self.assertIn("missing column", errors[0])
        rows, errors = import_service.parse_csv(
            self.upload(HEADER + "x,CI/CD,NOPE,High,Open,2026-10-02,d\n"))
        self.assertEqual(rows, [])
        self.assertIn("unknown technique_code", errors[0])
        rows, errors = import_service.parse_csv(self.upload("a", name="evil.exe"))
        self.assertTrue(errors)

    def test_tc06_bad_upload_does_not_crash_view(self):
        self.client.force_login(self.analyst)
        response = self.client.post(reverse("import_csv"), {"file": self.upload("\x00\x01garbage")})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Finding.objects.count(), 0)


class SecurityTests(BaseCase):
    def test_tc14_csrf_required(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.analyst)
        self.assertEqual(client.post(reverse("finding_add"), self.data()).status_code, 403)

    def test_tc15_script_is_escaped(self):
        Finding.objects.create(title="<script>alert(1)</script>", technique=self.tech,
                               date_found="2026-10-01")
        self.client.force_login(self.viewer)
        body = self.client.get(reverse("finding_list")).content.decode()
        self.assertNotIn("<script>alert(1)</script>", body)
        self.assertIn("&lt;script&gt;", body)

    def test_tc16_password_is_hashed(self):
        self.assertNotEqual(self.analyst.password, "pw-Test-12345")
        self.assertTrue(self.analyst.password.startswith(("pbkdf2_", "argon2", "scrypt", "bcrypt")))
