from django import forms
from django.core.validators import EmailValidator


class ContactForm(forms.Form):
    page_uri = forms.CharField(
        max_length=50,
        show_hidden_initial=True)
    name = forms.CharField(
        max_length=50,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form_input'})
    )
    email = forms.EmailField(
        max_length=100,
        validators=[EmailValidator],
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form_input'})
    )
    message = forms.CharField(
        max_length=10000,
        min_length=50,
        widget=forms.Textarea(attrs={'class': 'form_textarea'}),
        required=True
    )
