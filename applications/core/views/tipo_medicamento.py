from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import TipoMedicamento
from applications.core.forms.tipo_medicamento import TipoMedicamentoForm
from django.db.models import Q

class TipoMedicamentoListView(ListView):
    model = TipoMedicamento
    template_name = 'core/tipomedicamento/list.html'
    context_object_name = 'tipos'
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

class TipoMedicamentoCreateView(CreateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'core/tipomedicamento/form.html'
    success_url = reverse_lazy('core:tipomedicamento_list')

class TipoMedicamentoUpdateView(UpdateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'core/tipomedicamento/form.html'
    success_url = reverse_lazy('core:tipomedicamento_list')

class TipoMedicamentoDeleteView(DeleteView):
    model = TipoMedicamento
    template_name = 'core/tipomedicamento/confirm_delete.html'
    success_url = reverse_lazy('core:tipomedicamento_list')
