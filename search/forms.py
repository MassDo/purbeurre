from django import forms


class FoodSearchForm(forms.Form):
    """
        form for the research of a product
        with the autocompletion help.
    """
    user_input = forms.CharField(
        label='user_input',
        widget=forms.TextInput(attrs={'placeholder': 'Rechercher'}),
        required=True
    )