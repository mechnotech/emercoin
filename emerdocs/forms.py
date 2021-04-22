from django import forms


class SearchForm(forms.Form):

    find = forms.CharField(
        max_length=50,
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'search'})
    )
