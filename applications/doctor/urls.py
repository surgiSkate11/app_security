from django.urls import path

from applications.doctor.views.atenciones import AtencionListView, AtencionCreateView, AtencionUpdateView, \
    AtencionDeleteView
from applications.doctor.views.pagos import (
    PagoListView, PagoCreateView, PagoUpdateView,
    DetallePagoCreateView, DetallePagoUpdateView, PagoPayPalReturnView
)
from applications.doctor.views.api_calendar import api_pacientes, api_citas, api_horas_disponibles
from applications.doctor.views.citas import CalendarView


app_name='doctor' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Doctor
    path('atenciones/', AtencionListView.as_view(), name="atencion_list"),
    path('atenciones/create/', AtencionCreateView.as_view(), name="atencion_create"),
    path('atenciones/update/<int:pk>/', AtencionUpdateView.as_view(), name="atencion_update"),
    path('atenciones/delete/<int:pk>/', AtencionDeleteView.as_view(), name="atencion_delete"),


    # Rutas para vistas relacionadas con Pagos
    path('pagos/', PagoListView.as_view(), name="pago_list"),
    path('pagos/create/', PagoCreateView.as_view(), name="pago_create"),
    path('pagos/update/<int:pk>/', PagoUpdateView.as_view(), name="pago_update"),
    path('detalle_pago/create/', DetallePagoCreateView.as_view(), name="detalle_pago_create"),
    path('detalle_pago/update/<int:pk>/', DetallePagoUpdateView.as_view(), name="detalle_pago_update"),
    path('pago/paypal/return/', PagoPayPalReturnView.as_view(), name="pago_paypal_return"),


    # Rutas para vistas relacionadas con la API del calendario
    path('api/pacientes/', api_pacientes, name='api_pacientes'),
    path('api/citas/', api_citas, name='api_citas'),
    path('api/horas_disponibles/', api_horas_disponibles, name='api_horas_disponibles'),

    # Rutas para el calendario premium
    path('citas/', CalendarView.as_view(), name="citas"),
]