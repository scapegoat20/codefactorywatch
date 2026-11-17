from django import forms
from .models import Finding


class FindingForm(forms.ModelForm):
    class Meta:
        model = Finding
        fields = ["title", "description", "technique", "severity", "status", "date_found"]
        widgets = {"date_found": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
                   "description": forms.Textarea(attrs={"rows": 4})}

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Title is required.")
        return title


class CSVUploadForm(forms.Form):
    file = forms.FileField(label="CSV file")
