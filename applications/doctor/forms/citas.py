from django import forms
from django.utils import timezone
from applications.doctor.models import CitaMedica

class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['paciente', 'fecha', 'hora_cita', 'estado', 'observaciones']

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < timezone.now().date():
            raise forms.ValidationError("La fecha de la cita no puede ser en el pasado.")
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        paciente = cleaned_data.get('paciente')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora_cita')
        if not paciente:
            self.add_error('paciente', 'Debe seleccionar un paciente.')
        if not fecha:
            self.add_error('fecha', 'Debe ingresar una fecha.')
        if not hora:
            self.add_error('hora_cita', 'Debe ingresar una hora.')
        # Validar duplicidad de cita para el mismo paciente, fecha y hora
        if paciente and fecha and hora:
            existe = CitaMedica.objects.filter(paciente=paciente, fecha=fecha, hora_cita=hora)
            if self.instance.pk:
                existe = existe.exclude(pk=self.instance.pk)
            if existe.exists():
                raise forms.ValidationError('Ya existe una cita para este paciente en la misma fecha y hora.')
        return cleaned_data
