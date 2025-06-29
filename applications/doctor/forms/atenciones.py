from django import forms
from django.forms import ModelForm
from applications.doctor.models import Atencion
from applications.core.models import Paciente, Doctor
from applications.utils.widgets import MicrophoneTextarea


class AtencionForm(ModelForm):
    class Meta:
        model = Atencion
        fields = '__all__'

        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-select w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'doctor': forms.Select(attrs={
                'class': 'form-select w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'presion_arterial': forms.TextInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'placeholder': 'Ej: 120/80 mmHg'
            }),
            'pulso': forms.NumberInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'temperatura': forms.NumberInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'frecuencia_respiratoria': forms.NumberInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'saturacion_oxigeno': forms.NumberInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'altura': forms.NumberInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'motivo_consulta': MicrophoneTextarea(attrs={
                'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'rows': 3
            }),
            'sintomas': MicrophoneTextarea(attrs={
                'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'rows': 3
            }),
            'tratamiento': MicrophoneTextarea(attrs={
                'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'rows': 3
            }),
            'diagnostico': forms.SelectMultiple(attrs={
                'class': 'form-multiselect w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'examen_fisico': MicrophoneTextarea(attrs={
                'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'rows': 2
            }),
            'examenes_enviados': MicrophoneTextarea(attrs={
                'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'rows': 2
            }),
            'comentario_adicional': MicrophoneTextarea(attrs={
                'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'rows': 2
            }),
            'es_control': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-blue-600'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Filtrar pacientes activos
        self.fields['paciente'].queryset = Paciente.active_patient.all()
        # Filtrar doctores activos según el usuario
        if self.user:
            if hasattr(self.user, 'doctor'):
                self.fields['doctor'].queryset = Doctor.objects.filter(pk=self.user.doctor.pk, activo=True)
                self.fields['doctor'].initial = self.user.doctor.pk
                self.fields['doctor'].disabled = True
            elif self.user.groups.filter(name='Asistentes').exists():
                self.fields['doctor'].queryset = Doctor.objects.filter(activo=True)
            else:
                self.fields['doctor'].queryset = Doctor.objects.none()
        else:
            self.fields['doctor'].queryset = Doctor.objects.filter(activo=True)

    def clean(self):
        cleaned_data = super().clean()
        paciente = cleaned_data.get('paciente')
        doctor = cleaned_data.get('doctor')
        # Validar paciente activo
        if paciente and not paciente.activo:
            self.add_error('paciente', 'El paciente no está activo.')
        # Validar doctor activo
        if doctor and not doctor.activo:
            self.add_error('doctor', 'El doctor no está activo.')
        if not paciente:
            self.add_error('paciente', 'Debe seleccionar un paciente.')
        if not doctor:
            self.add_error('doctor', 'Debe seleccionar un doctor.')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Asignar automáticamente el doctor si es doctor autenticado
        if self.user and hasattr(self.user, 'doctor'):
            instance.doctor = self.user.doctor
        if commit:
            instance.save()
            self.save_m2m()
        return instance
