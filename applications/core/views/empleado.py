from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import Empleado
from applications.core.forms.empleado import EmpleadoForm
from django.db.models import Q

class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'core/empleado/list.html'
    context_object_name = 'empleados'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombres__icontains=search) |
                Q(apellidos__icontains=search) |
                Q(cedula_ecuatoriana__icontains=search)
            )
        return queryset

class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'core/empleado/form.html'
    success_url = reverse_lazy('core:empleado_list')

class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'core/empleado/form.html'
    success_url = reverse_lazy('core:empleado_list')

class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'core/empleado/confirm_delete.html'
    success_url = reverse_lazy('core:empleado_list')
