from django import forms
from .models import Repository


class RepoForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = ["repo_name","username", "stars", "language", "url", "created_at"]