from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import Cargo
from applications.core.forms.cargo import CargoForm
from django.db.models import Q

class CargoListView(ListView):
    model = Cargo
    template_name = 'core/cargo/list.html'
    context_object_name = 'cargos'
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

class CargoCreateView(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'core/cargo/form.html'
    success_url = reverse_lazy('core:cargo_list')

class CargoUpdateView(UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'core/cargo/form.html'
    success_url = reverse_lazy('core:cargo_list')

class CargoDeleteView(DeleteView):
    model = Cargo
    template_name = 'core/cargo/confirm_delete.html'
    success_url = reverse_lazy('core:cargo_list')
