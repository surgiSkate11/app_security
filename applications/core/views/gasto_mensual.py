from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import GastoMensual
from applications.core.forms.gasto_mensual import GastoMensualForm
from django.db.models import Q
from applications.doctor.utils.auditorias import registrar_auditoria
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from applications.core.models import Doctor

class GastoMensualListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = GastoMensual
    template_name = 'core/gasto_mensual/list.html'
    context_object_name = 'gastos'
    paginate_by = 10
    permission_required = 'core.view_gasto_mensual'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        user = self.request.user
        # Si es médico, solo ve sus propios gastos
        if user.is_superuser or user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Asistentes').exists():
            pass
        elif user.groups.filter(name='Médicos').exists():
            try:
                doctor = Doctor.objects.get(email=user.email)
                queryset = queryset.filter(doctor=doctor)
            except Doctor.DoesNotExist:
                queryset = queryset.none()
        else:
            queryset = queryset.none()
        if search:
            queryset = queryset.filter(
                Q(tipo_gasto__nombre__icontains=search) |
                Q(valor__icontains=search) |
                Q(observacion__icontains=search)
            )
        return queryset

class GastoMensualCreateView(CreateView):
    model = GastoMensual
    form_class = GastoMensualForm
    template_name = 'core/gasto_mensual/form.html'
    success_url = reverse_lazy('core:gasto_mensual_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_auditoria(self.request, 'GastoMensual', self.object.id, 'CREAR')
        return response

class GastoMensualUpdateView(UpdateView):
    model = GastoMensual
    form_class = GastoMensualForm
    template_name = 'core/gasto_mensual/form.html'
    success_url = reverse_lazy('core:gasto_mensual_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_auditoria(self.request, 'GastoMensual', self.object.id, 'EDITAR')
        return response

class GastoMensualDeleteView(DeleteView):
    model = GastoMensual
    template_name = 'core/gasto_mensual/confirm_delete.html'
    success_url = reverse_lazy('core:gasto_mensual_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        registrar_auditoria(request, 'GastoMensual', obj.id, 'ELIMINAR')
        return response
