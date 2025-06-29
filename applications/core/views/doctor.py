from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import Doctor
from applications.core.forms.doctor import DoctorForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class DoctorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Doctor
    template_name = 'core/doctor/list.html'
    context_object_name = 'doctores'
    paginate_by = 10
    permission_required = 'core.view_doctor'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        user = self.request.user
        # Si no es admin, solo ve su propio perfil
        if user.is_superuser or user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Asistentes').exists():
            pass
        elif user.groups.filter(name='Médicos').exists():
            try:
                doctor = Doctor.objects.get(email=user.email)
                queryset = queryset.filter(id=doctor.id)
            except Doctor.DoesNotExist:
                queryset = queryset.none()
        else:
            queryset = queryset.none()
        if search:
            queryset = queryset.filter(
                Q(nombres__icontains=search) |
                Q(apellidos__icontains=search) |
                Q(ruc__icontains=search)
            )
        return queryset

class DoctorCreateView(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctor/form.html'
    success_url = reverse_lazy('core:doctor_list')

class DoctorUpdateView(UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctor/form.html'
    success_url = reverse_lazy('core:doctor_list')

class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'core/doctor/confirm_delete.html'
    success_url = reverse_lazy('core:doctor_list')
