from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import TipoSangre
from applications.core.forms.tipo_sangre import TipoSangreForm
from django.db.models import Q

class TipoSangreListView(ListView):
    model = TipoSangre
    template_name = 'core/tiposangre/list.html'
    context_object_name = 'tipos_sangre'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(tipo__icontains=search) |
                Q(descripcion__icontains=search)
            )
        return queryset

class TipoSangreCreateView(CreateView):
    model = TipoSangre
    form_class = TipoSangreForm
    template_name = 'core/tiposangre/form.html'
    success_url = reverse_lazy('core:tiposangre_list')

class TipoSangreUpdateView(UpdateView):
    model = TipoSangre
    form_class = TipoSangreForm
    template_name = 'core/tiposangre/form.html'
    success_url = reverse_lazy('core:tiposangre_list')

class TipoSangreDeleteView(DeleteView):
    model = TipoSangre
    template_name = 'core/tiposangre/confirm_delete.html'
    success_url = reverse_lazy('core:tiposangre_list')
