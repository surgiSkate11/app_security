from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import GastoMensual
from applications.core.forms.gasto_mensual import GastoMensualForm
from django.db.models import Q

class GastoMensualListView(ListView):
    model = GastoMensual
    template_name = 'core/gastomensual/list.html'
    context_object_name = 'gastos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
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
    template_name = 'core/gastomensual/form.html'
    success_url = reverse_lazy('core:gastomensual_list')

class GastoMensualUpdateView(UpdateView):
    model = GastoMensual
    form_class = GastoMensualForm
    template_name = 'core/gastomensual/form.html'
    success_url = reverse_lazy('core:gastomensual_list')

class GastoMensualDeleteView(DeleteView):
    model = GastoMensual
    template_name = 'core/gastomensual/confirm_delete.html'
    success_url = reverse_lazy('core:gastomensual_list')
