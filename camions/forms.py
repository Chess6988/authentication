import re
from django import forms
from .models import Truck, RubberTransport

class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = ['matriculation_number']
        widgets = {
            'matriculation_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter matriculation number'}),
        }
    def clean_matriculation_number(self):
        matriculation_number = self.cleaned_data.get('matriculation_number')
        if not re.match(r'^[A-Z]{2}-\d{3}-[A-Z]{2}$', matriculation_number):
            raise forms.ValidationError('Matriculation number must follow the format "GA-456-TY".')
        return matriculation_number

class RubberTransportForm(forms.ModelForm):
    class Meta:
        model = RubberTransport
        fields = ['tons_of_rubber', 'price_per_ton']
        widgets = {
            'tons_of_rubber': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'price_per_ton': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
