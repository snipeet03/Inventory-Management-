from django.forms import ModelForm
from django import forms
from .models import ExardProduct 



class AddExhardForm(forms.Form):
    alpha_number = forms.ModelChoiceField(
        queryset=ExardProduct.objects.all(),
        label="Alpha Number",
        widget=forms.Select(attrs={'class': 'select2', 'id': 'id_alpha_number'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        label="Quantity to Add",
        widget=forms.NumberInput(attrs={
            'class': 'form-control bg-white text-dark'
        })
    )


