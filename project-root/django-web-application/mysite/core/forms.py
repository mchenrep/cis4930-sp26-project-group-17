from django import forms
from .models import Repository


class RepoForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = ["full_name", "stars", "language", "url", "created_at"]