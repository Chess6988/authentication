from django import forms
from .models import Truck

class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = ['matriculation_number']
        widgets = {
            'matriculation_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter matriculation number'}),
        }
