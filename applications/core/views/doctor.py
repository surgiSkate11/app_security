from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import Doctor
from applications.core.forms.doctor import DoctorForm
from django.db.models import Q

class DoctorListView(ListView):
    model = Doctor
    template_name = 'core/doctor/list.html'
    context_object_name = 'doctores'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(nombres__icontains=search) |
                Q(apellidos__icontains=search) |
                Q(ruc__icontains=search)
            )
        return queryset

class DoctorCreateView(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctor/form.html'
    success_url = reverse_lazy('core:doctor_list')

class DoctorUpdateView(UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctor/form.html'
    success_url = reverse_lazy('core:doctor_list')

class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'core/doctor/confirm_delete.html'
    success_url = reverse_lazy('core:doctor_list')
