from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from applications.doctor.models import CitaMedica, ServiciosAdicionales
from applications.doctor.forms.citas import CitaMedicaForm
from applications.doctor.forms.servicios import ServiciosAdicionalesForm
from applications.core.models import Doctor

class CitaMedicaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CitaMedica
    template_name = 'doctor/citas/list.html'
    context_object_name = 'citas'
    paginate_by = 10
    permission_required = 'doctor.view_citamedica'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Asistentes').exists():
            pass  # ve todo
        elif user.groups.filter(name='Médicos').exists():
            try:
                doctor = Doctor.objects.get(email=user.email)
                qs = qs.filter(doctor=doctor)
            except Doctor.DoesNotExist:
                qs = qs.none()
        else:
            qs = qs.none()
        if q:
            qs = qs.filter(paciente__nombre_completo__icontains=q)
        return qs.order_by('-fecha', '-hora_cita')

class CitaMedicaCreateView(CreateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'doctor/citas/form.html'
    success_url = reverse_lazy('doctor:cita_list')

class CitaMedicaUpdateView(UpdateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'doctor/citas/form.html'
    success_url = reverse_lazy('doctor:cita_list')

class ServiciosAdicionalesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ServiciosAdicionales
    template_name = 'doctor/servicios/list.html'
    context_object_name = 'servicios'
    paginate_by = 10
    permission_required = 'doctor.view_serviciosadicionales'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(nombre_servicio__icontains=q)
        return qs.order_by('nombre_servicio')

class ServiciosAdicionalesCreateView(CreateView):
    model = ServiciosAdicionales
    form_class = ServiciosAdicionalesForm
    template_name = 'doctor/servicios/form.html'
    success_url = reverse_lazy('doctor:servicio_list')

class ServiciosAdicionalesUpdateView(UpdateView):
    model = ServiciosAdicionales
    form_class = ServiciosAdicionalesForm
    template_name = 'doctor/servicios/form.html'
    success_url = reverse_lazy('doctor:servicio_list')
