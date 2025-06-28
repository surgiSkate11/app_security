from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import Especialidad
from applications.core.forms.especialidad import EspecialidadForm
from django.db.models import Q

class EspecialidadListView(ListView):
    model = Especialidad
    template_name = 'core/especialidad/list.html'
    context_object_name = 'especialidades'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search)
            )
        return queryset

class EspecialidadCreateView(CreateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'core/especialidad/form.html'
    success_url = reverse_lazy('core:especialidad_list')

class EspecialidadUpdateView(UpdateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'core/especialidad/form.html'
    success_url = reverse_lazy('core:especialidad_list')

class EspecialidadDeleteView(DeleteView):
    model = Especialidad
    template_name = 'core/especialidad/confirm_delete.html'
    success_url = reverse_lazy('core:especialidad_list')
