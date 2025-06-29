from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from applications.doctor.models import Pago, DetallePago, ServiciosAdicionales
from applications.doctor.forms.pagos import PagoForm, DetallePagoForm
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from applications.doctor.utils.paypal_api import PayPalAPI
from django.views import View
from django.http import HttpResponse
import json
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from applications.core.models import Doctor

class PagoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Pago
    template_name = 'doctor/pagos/list.html'
    context_object_name = 'pagos'
    paginate_by = 10
    permission_required = 'doctor.view_pago'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Asistentes').exists():
            pass  # ve todo
        elif user.groups.filter(name='Médicos').exists():
            try:
                doctor = Doctor.objects.get(email=user.email)
                qs = qs.filter(atencion__doctor=doctor)
            except Doctor.DoesNotExist:
                qs = qs.none()
        else:
            qs = qs.none()
        if q:
            qs = qs.filter(nombre_pagador__icontains=q)
        return qs.order_by('-fecha_creacion')

class PagoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Pago
    form_class = PagoForm
    template_name = 'doctor/pagos/form.html'
    success_url = reverse_lazy('doctor:pago_list')
    permission_required = 'doctor.add_pago'

    def form_valid(self, form):
        detalles_data = self.request.POST.get('detalles_data')
        detalles = json.loads(detalles_data) if detalles_data else []
        metodo = form.cleaned_data.get('metodo_pago')
        if metodo == 'paypal':
            # Crear orden en PayPal y redirigir
            total = form.cleaned_data.get('monto_total')
            paypal = PayPalAPI()
            return_url = self.request.build_absolute_uri(reverse('doctor:pago_paypal_return'))
            cancel_url = self.request.build_absolute_uri(reverse('doctor:pago_create'))
            order = paypal.create_order(amount=total, return_url=return_url, cancel_url=cancel_url)
            for link in order['links']:
                if link['rel'] == 'approve':
                    self.request.session['pago_form_data'] = form.cleaned_data
                    self.request.session['pago_detalles'] = detalles
                    return redirect(link['href'])
        # Otros métodos: flujo normal
        from applications.doctor.utils.transacciones_pago import crear_pago_con_detalles
        data = form.cleaned_data.copy()
        data['created_by'] = self.request.user
        data['updated_by'] = self.request.user
        crear_pago_con_detalles(self.request, data, detalles)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios'] = ServiciosAdicionales.objects.filter(activo=True)
        return context

class PagoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Pago
    form_class = PagoForm
    template_name = 'doctor/pagos/form.html'
    success_url = reverse_lazy('doctor:pago_list')
    permission_required = 'doctor.change_pago'

    def form_valid(self, form):
        detalles_data = self.request.POST.get('detalles_data')
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

# Vista para manejar el retorno de PayPal
class PagoPayPalReturnView(View):
    def get(self, request):
        order_id = request.GET.get('token')
        if not order_id:
            return HttpResponse('Error: No se recibió token de PayPal', status=400)
        paypal = PayPalAPI()
        capture = paypal.capture_order(order_id)
        # Recuperar datos del pago desde la sesión
        data = request.session.pop('pago_form_data', None)
        detalles = request.session.pop('pago_detalles', None)
        if not data or not detalles:
            return HttpResponse('Error: No se encontró información del pago en sesión', status=400)
        # Marcar como pagado si la captura fue exitosa
        data['estado'] = 'pagado'
        from applications.doctor.utils.transacciones_pago import crear_pago_con_detalles
        crear_pago_con_detalles(request, data, detalles)
        return redirect('doctor:pago_list')
