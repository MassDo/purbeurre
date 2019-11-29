from django import forms
from product.models import Product


class FoodSearchForm(forms.Form):
    """
        form for the research of a product
        with the autocompletion help.
    """
    user_input = forms.CharField(
        label='choisissez un aliment',
        required=False
    )