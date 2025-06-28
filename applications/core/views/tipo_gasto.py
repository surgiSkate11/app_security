from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import TipoGasto
from applications.core.forms.tipo_gasto import TipoGastoForm
from django.db.models import Q

class TipoGastoListView(ListView):
    model = TipoGasto
    template_name = 'core/tipo_gasto/list.html'
    context_object_name = 'tipos_gasto'
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

class TipoGastoCreateView(CreateView):
    model = TipoGasto
    form_class = TipoGastoForm
    template_name = 'core/tipo_gasto/form.html'
    success_url = reverse_lazy('core:tipogasto_list')

class TipoGastoUpdateView(UpdateView):
    model = TipoGasto
    form_class = TipoGastoForm
    template_name = 'core/tipo_gasto/form.html'
    success_url = reverse_lazy('core:tipogasto_list')

class TipoGastoDeleteView(DeleteView):
    model = TipoGasto
    template_name = 'core/tipo_gasto/confirm_delete.html'
    success_url = reverse_lazy('core:tipogasto_list')
