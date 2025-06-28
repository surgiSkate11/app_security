from django import forms
from applications.core.models import GastoMensual

class GastoMensualForm(forms.ModelForm):
    class Meta:
        model = GastoMensual
        fields = '__all__'
        widgets = {
            'tipo_gasto': forms.Select(attrs={'class': 'form-input', 'required': True}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-input', 'required': True}),
            'valor': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': '0.01', 'required': True}),
            'observacion': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }
        error_messages = {
            'tipo_gasto': {'required': 'El tipo de gasto es obligatorio.'},
            'fecha': {'required': 'La fecha es obligatoria.'},
            'valor': {'required': 'El valor es obligatorio.'},
        }
