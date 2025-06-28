from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import Medicamento
from applications.core.forms.medicamento import MedicamentoForm
from django.db.models import Q

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

class MedicamentoUpdateView(UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'core/medicamento/form.html'
    success_url = reverse_lazy('core:medicamento_list')

class MedicamentoDeleteView(DeleteView):
    model = Medicamento
    template_name = 'core/medicamento/confirm_delete.html'
    success_url = reverse_lazy('core:medicamento_list')
