from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from applications.doctor.models import CitaMedica
from applications.doctor.forms.citas import CitaMedicaForm

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
