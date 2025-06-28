from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from applications.doctor.models import Pago, DetallePago, ServiciosAdicionales
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

    def form_valid(self, form):
        detalles_data = self.request.POST.get('detalles_data')
        # detalles_data debe ser una lista de dicts (puedes obtenerla de un campo oculto, JSON, etc.)
        import json
        detalles = json.loads(detalles_data) if detalles_data else []
        from applications.doctor.utils.transacciones_pago import crear_pago_con_detalles
        # Añadir usuario de auditoría
        data = form.cleaned_data.copy()
        data['created_by'] = self.request.user
        data['updated_by'] = self.request.user
        crear_pago_con_detalles(self.request, data, detalles)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios'] = ServiciosAdicionales.objects.filter(activo=True)
        return context

class PagoUpdateView(UpdateView):
    model = Pago
    form_class = PagoForm
    template_name = 'doctor/pagos/form.html'
    success_url = reverse_lazy('doctor:pago_list')

    def form_valid(self, form):
        detalles_data = self.request.POST.get('detalles_data')
        import json
        detalles = json.loads(detalles_data) if detalles_data else []
        from applications.doctor.utils.transacciones_pago import actualizar_pago_con_detalles
        data = form.cleaned_data.copy()
        data['updated_by'] = self.request.user
        actualizar_pago_con_detalles(self.request, self.object.id, data, detalles)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios'] = ServiciosAdicionales.objects.filter(activo=True)
        return context

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
