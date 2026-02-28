from django import forms
from .models import Complaint, Category

class ComplaintForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="-- Select Category --",
        widget=forms.Select(attrs={"class": "border rounded px-3 py-2 w-full"})
    )

    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category', 'priority', 'attachment']