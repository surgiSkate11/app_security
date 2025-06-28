from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import Diagnostico
from applications.core.forms.diagnostico import DiagnosticoForm
from django.db.models import Q

class DiagnosticoListView(ListView):
    model = Diagnostico
    template_name = 'core/diagnostico/list.html'
    context_object_name = 'diagnosticos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) |
                Q(descripcion__icontains=search) |
                Q(datos_adicionales__icontains=search)
            )
        return queryset

class DiagnosticoCreateView(CreateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'core/diagnostico/form.html'
    success_url = reverse_lazy('core:diagnostico_list')

class DiagnosticoUpdateView(UpdateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'core/diagnostico/form.html'
    success_url = reverse_lazy('core:diagnostico_list')

class DiagnosticoDeleteView(DeleteView):
    model = Diagnostico
    template_name = 'core/diagnostico/confirm_delete.html'
    success_url = reverse_lazy('core:diagnostico_list')
