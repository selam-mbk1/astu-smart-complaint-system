from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'department', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔒 Remove admin from public registration
        self.fields['role'].choices = [
            choice for choice in User.ROLE_CHOICES
            if choice[0] != 'admin'
        ]

        self.fields['email'].required = True

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'border p-2 w-full rounded mb-3'
            })

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        department = cleaned_data.get("department")

        if role == "staff" and not department:
            raise forms.ValidationError("Staff must provide a department.")

        return cleaned_data