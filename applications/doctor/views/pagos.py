from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from applications.doctor.models import Pago, DetallePago
from applications.doctor.forms.pagos import PagoForm, DetallePagoForm

class PagoListView(ListView):
    model = Pago
    template_name = 'doctor/pagos/list.html'
    context_object_name = 'pagos'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        qs = super().get_queryset()
        if q:
            qs = qs.filter(nombre_pagador__icontains=q)
        return qs.order_by('-fecha_creacion')

class PagoCreateView(CreateView):
    model = Pago
    form_class = PagoForm
    template_name = 'doctor/pagos/form.html'
    success_url = reverse_lazy('doctor:pago_list')

class PagoUpdateView(UpdateView):
    model = Pago
    form_class = PagoForm
    template_name = 'doctor/pagos/form.html'
    success_url = reverse_lazy('doctor:pago_list')

class DetallePagoCreateView(CreateView):
    model = DetallePago
    form_class = DetallePagoForm
    template_name = 'doctor/pagos/detalle_form.html'
    success_url = reverse_lazy('doctor:pago_list')

class DetallePagoUpdateView(UpdateView):
    model = DetallePago
    form_class = DetallePagoForm
    template_name = 'doctor/pagos/detalle_form.html'
    success_url = reverse_lazy('doctor:pago_list')
