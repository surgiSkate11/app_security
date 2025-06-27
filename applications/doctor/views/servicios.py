from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from applications.doctor.models import CitaMedica, ServiciosAdicionales
from applications.doctor.forms.citas import CitaMedicaForm
from applications.doctor.forms.servicios import ServiciosAdicionalesForm

class CitaMedicaListView(ListView):
    model = CitaMedica
    template_name = 'doctor/citas/list.html'
    context_object_name = 'citas'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        qs = super().get_queryset()
        if q:
            qs = qs.filter(paciente__nombre_completo__icontains=q)
        return qs.order_by('-fecha', '-hora_cita')

class CitaMedicaCreateView(CreateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'doctor/citas/form.html'
    success_url = reverse_lazy('doctor:cita_list')

class CitaMedicaUpdateView(UpdateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'doctor/citas/form.html'
    success_url = reverse_lazy('doctor:cita_list')

class ServiciosAdicionalesListView(ListView):
    model = ServiciosAdicionales
    template_name = 'doctor/servicios/list.html'
    context_object_name = 'servicios'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        qs = super().get_queryset()
        if q:
            qs = qs.filter(nombre_servicio__icontains=q)
        return qs.order_by('nombre_servicio')

class ServiciosAdicionalesCreateView(CreateView):
    model = ServiciosAdicionales
    form_class = ServiciosAdicionalesForm
    template_name = 'doctor/servicios/form.html'
    success_url = reverse_lazy('doctor:servicio_list')

class ServiciosAdicionalesUpdateView(UpdateView):
    model = ServiciosAdicionales
    form_class = ServiciosAdicionalesForm
    template_name = 'doctor/servicios/form.html'
    success_url = reverse_lazy('doctor:servicio_list')
