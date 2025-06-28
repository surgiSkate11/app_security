from django.urls import path

from applications.doctor.views.atenciones import AtencionListView, AtencionCreateView, AtencionUpdateView, \
    AtencionDeleteView
from applications.doctor.views.citas import CitaMedicaListView, CitaMedicaCreateView, CitaMedicaUpdateView
from applications.doctor.views.pagos import (
    PagoListView, PagoCreateView, PagoUpdateView,
    DetallePagoCreateView, DetallePagoUpdateView
)

app_name='doctor' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Doctor
    path('atencion_list/', AtencionListView.as_view(), name="atencion_list"),
    path('atencion_create/', AtencionCreateView.as_view(), name="atencion_create"),
    path('atencion_update/<int:pk>/', AtencionUpdateView.as_view(), name="atencion_update"),
    path('atencion_delete/<int:pk>/', AtencionDeleteView.as_view(), name="atencion_delete"),
    
    
    # Rutas para vistas relacionadas con Cita Medica
    path('cita_list/', CitaMedicaListView.as_view(), name="cita_list"),
    path('cita_create/', CitaMedicaCreateView.as_view(), name="cita_create"),
    path('cita_update/<int:pk>/', CitaMedicaUpdateView.as_view(), name="cita_update"),

    # Rutas para vistas relacionadas con Pagos
    path('pagos_list/', PagoListView.as_view(), name="pago_list"),
    path('pago_create/', PagoCreateView.as_view(), name="pago_create"),
    path('pago_update/<int:pk>/', PagoUpdateView.as_view(), name="pago_update"),
    path('detalle_pago_create/', DetallePagoCreateView.as_view(), name="detalle_pago_create"),
    path('detalle_pago_update/<int:pk>/', DetallePagoUpdateView.as_view(), name="detalle_pago_update"),
]