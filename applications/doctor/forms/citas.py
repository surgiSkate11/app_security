from django import forms
from django.utils import timezone
from applications.doctor.models import CitaMedica
from applications.core.models import Paciente
from applications.core.models import Doctor
from applications.doctor.utils.horarios import obtener_horarios_disponibles_para_fecha
from django.forms import ChoiceField

class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['paciente', 'doctor', 'fecha', 'hora_cita', 'estado', 'observaciones']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Filtrar pacientes activos
        self.fields['paciente'].queryset = Paciente.active_patient.all()
        # Filtrar doctores activos según el usuario
        if self.user:
            if hasattr(self.user, 'doctor'):
                # Si es doctor, solo puede asignarse a sí mismo
                self.fields['doctor'].queryset = Doctor.objects.filter(pk=self.user.doctor.pk, activo=True)
                self.fields['doctor'].initial = self.user.doctor.pk
                self.fields['doctor'].disabled = True
            elif self.user.groups.filter(name='Asistentes').exists():
                # Si es asistente, puede ver todos los doctores activos
                self.fields['doctor'].queryset = Doctor.objects.filter(activo=True)
            else:
                # Otros usuarios no pueden asignar doctores
                self.fields['doctor'].queryset = Doctor.objects.none()
        else:
            self.fields['doctor'].queryset = Doctor.objects.filter(activo=True)
        # --- Lógica para el select de horas disponibles ---
        doctor = None
        if self.user and hasattr(self.user, 'doctor'):
            doctor = self.user.doctor
        elif 'doctor' in self.initial:
            doctor = self.initial['doctor']
        elif 'doctor' in self.data:
            try:
                doctor = Doctor.objects.get(pk=self.data['doctor'])
            except Exception:
                doctor = None
        fecha = self.initial.get('fecha') or self.data.get('fecha')
        if doctor and fecha:
            import datetime
            if isinstance(fecha, str):
                try:
                    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
                except Exception:
                    fecha = None
            if fecha:
                from applications.doctor.models import CitaMedica
                citas_ocupadas = CitaMedica.objects.filter(doctor=doctor, fecha=fecha).values_list('hora_cita', flat=True)
                horas = obtener_horarios_disponibles_para_fecha(doctor, fecha, list(citas_ocupadas))
                self.fields['hora_cita'] = ChoiceField(
                    choices=[(h.strftime('%H:%M'), h.strftime('%H:%M')) for h in horas],
                    required=True,
                    label='Hora de la Cita'
                )
        # Si no hay doctor o fecha, dejar el campo vacío
        else:
            self.fields['hora_cita'] = ChoiceField(choices=[], required=True, label='Hora de la Cita')

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < timezone.now().date():
            raise forms.ValidationError("La fecha de la cita no puede ser en el pasado.")
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        paciente = cleaned_data.get('paciente')
        doctor = cleaned_data.get('doctor')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora_cita')
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
        if not fecha:
            self.add_error('fecha', 'Debe ingresar una fecha.')
        if not hora:
            self.add_error('hora_cita', 'Debe ingresar una hora.')
        # Validar duplicidad de cita para el mismo doctor, fecha y hora
        if doctor and fecha and hora:
            existe = CitaMedica.objects.filter(doctor=doctor, fecha=fecha, hora_cita=hora)
            if self.instance.pk:
                existe = existe.exclude(pk=self.instance.pk)
            if existe.exists():
                raise forms.ValidationError('Ya existe una cita para este doctor en la misma fecha y hora.')
        # Validar duplicidad de cita para el mismo paciente, fecha y hora
        if paciente and fecha and hora:
            existe = CitaMedica.objects.filter(paciente=paciente, fecha=fecha, hora_cita=hora)
            if self.instance.pk:
                existe = existe.exclude(pk=self.instance.pk)
            if existe.exists():
                raise forms.ValidationError('Ya existe una cita para este paciente en la misma fecha y hora.')
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
