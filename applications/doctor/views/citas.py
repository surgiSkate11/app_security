from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from applications.doctor.models import CitaMedica
from applications.core.models import Doctor

class CalendarView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'doctor/citas/citas.html'
    permission_required = 'doctor.view_citamedica'

    def dispatch(self, request, *args, **kwargs):
        # Solo usuarios con grupo adecuado pueden acceder
        user = request.user
        if not (user.is_superuser or user.groups.filter(name__in=['Administrador', 'Médicos', 'Asistentes']).exists()):
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Administrador o superusuario: todas las citas
        if user.is_superuser or user.groups.filter(name='Administrador').exists():
            context['citas'] = CitaMedica.objects.all()
        # Médicos: solo sus citas (por email)
        elif user.groups.filter(name='Médicos').exists():
            try:
                doctor = Doctor.objects.get(email=user.email)
                context['citas'] = CitaMedica.objects.filter(doctor=doctor)
            except Doctor.DoesNotExist:
                context['citas'] = CitaMedica.objects.none()
        # Asistentes: todas las citas
        elif user.groups.filter(name='Asistentes').exists():
            context['citas'] = CitaMedica.objects.all()
        else:
            context['citas'] = CitaMedica.objects.none()
        # Agregar los grupos del usuario autenticado para el header (solo si no existe ya en el contexto)
        if 'group_list' not in context:
            context['group_list'] = user.groups.all()
        return context
