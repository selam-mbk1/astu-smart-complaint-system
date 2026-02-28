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
        fields = ['title', 'description', 'category', 'priority', 'attachment', 'dorm_block' , 'building_name',  'course_code' ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initially hide location fields
        self.fields['dorm_block'].required = False
        self.fields['building_name'].required = False
        self.fields['course_code'].required = False

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add styling
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'border p-2 w-full rounded mb-3'
            })

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Category.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Category with this name already exists.")
        return name