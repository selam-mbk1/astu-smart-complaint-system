from django import forms
from .models import ChatbotFAQ

class ChatbotFAQForm(forms.ModelForm):
    class Meta:
        model = ChatbotFAQ
        fields = ['question', 'answer', 'keywords']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'border p-2 w-full rounded mb-3'
            })