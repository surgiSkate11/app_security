from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import MarcaMedicamento
from applications.core.forms.marca_medicamento import MarcaMedicamentoForm
from django.db.models import Q

class MarcaMedicamentoListView(ListView):
    model = MarcaMedicamento
    template_name = 'core/marcamedicamento/list.html'
    context_object_name = 'marcas'
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

class MarcaMedicamentoCreateView(CreateView):
    model = MarcaMedicamento
    form_class = MarcaMedicamentoForm
    template_name = 'core/marcamedicamento/form.html'
    success_url = reverse_lazy('core:marcamedicamento_list')

class MarcaMedicamentoUpdateView(UpdateView):
    model = MarcaMedicamento
    form_class = MarcaMedicamentoForm
    template_name = 'core/marcamedicamento/form.html'
    success_url = reverse_lazy('core:marcamedicamento_list')

class MarcaMedicamentoDeleteView(DeleteView):
    model = MarcaMedicamento
    template_name = 'core/marcamedicamento/confirm_delete.html'
    success_url = reverse_lazy('core:marcamedicamento_list')
