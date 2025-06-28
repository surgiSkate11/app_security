from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import Medicamento
from applications.core.forms.medicamento import MedicamentoForm
from django.db.models import Q
from applications.doctor.utils.auditorias import registrar_auditoria

class MedicamentoListView(ListView):
    model = Medicamento
    template_name = 'core/medicamento/list.html'
    context_object_name = 'medicamentos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search) |
                Q(concentracion__icontains=search)
            )
        return queryset

class MedicamentoCreateView(CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'core/medicamento/form.html'
    success_url = reverse_lazy('core:medicamento_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_auditoria(self.request, 'Medicamento', self.object.id, 'CREAR')
        return response

class MedicamentoUpdateView(UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'core/medicamento/form.html'
    success_url = reverse_lazy('core:medicamento_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_auditoria(self.request, 'Medicamento', self.object.id, 'EDITAR')
        return response

class MedicamentoDeleteView(DeleteView):
    model = Medicamento
    template_name = 'core/medicamento/confirm_delete.html'
    success_url = reverse_lazy('core:medicamento_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        object_id = self.object.id
        response = super().delete(request, *args, **kwargs)
        registrar_auditoria(request, 'Medicamento', object_id, 'ELIMINAR')
        return response
