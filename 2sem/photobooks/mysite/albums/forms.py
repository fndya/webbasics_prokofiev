# albums/forms.py
from django import forms
from .models import Album

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        # можно не все поля, задание этого не требует
        fields = ["title", "format", "cover_type", "status", "cover_photo", "page_count"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "page_count": forms.NumberInput(attrs={"class": "form-input"}),
            "format": forms.Select(attrs={"class": "form-input"}),
            "cover_type": forms.Select(attrs={"class": "form-input"}),
            "status": forms.Select(attrs={"class": "form-input"}),
            "cover_photo": forms.Select(attrs={"class": "form-input"}),
        }
