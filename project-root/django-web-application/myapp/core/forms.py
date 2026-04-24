from django import forms
from .models import Repository


class RepositoryForm(forms.ModelForm):
    """Create / edit form for a Repository. Bootstrap 5 classes applied."""

    class Meta:
        model = Repository
        fields = ['repo_name', 'owner', 'language', 'stars', 'url', 'created_at', 'source']
        widgets = {
            'repo_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. django',
            }),
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'language': forms.Select(attrs={'class': 'form-select'}),
            'stars': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/owner/repo',
            }),
            'created_at': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'source': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_stars(self):
        stars = self.cleaned_data.get('stars')
        if stars is not None and stars < 0:
            raise forms.ValidationError("Stars cannot be negative.")
        return stars