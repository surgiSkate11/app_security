from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views import View
from applications.core.models import Paciente, Doctor
from applications.doctor.models import CitaMedica
from django.contrib.auth import get_user_model
import json
from datetime import datetime
from applications.doctor.utils.horarios import obtener_horarios_disponibles_para_fecha

@login_required
@permission_required('doctor.view_paciente', raise_exception=True)
def api_pacientes(request):
    doctor_id = request.GET.get('doctor_id')
    # Solo doctores o asistentes pueden consultar
    if not (request.user.is_superuser or hasattr(request.user, 'doctor') or request.user.groups.filter(name='Asistentes').exists()):
        return JsonResponse({'error': 'No autorizado'}, status=403)
    if request.method == 'GET':
        # Si es doctor, solo sus pacientes
        if hasattr(request.user, 'doctor'):
            pacientes = Paciente.active_patient.filter(doctor=request.user.doctor)
        elif request.user.groups.filter(name='Asistentes').exists():
            pacientes = Paciente.active_patient.all()
        else:
            pacientes = Paciente.objects.none()
        data = [
            {'id': p.id, 'nombre': f"{p.nombres} {p.apellidos}", 'direccion': p.direccion, 'telefono': p.telefono, 'email': p.email}
            for p in pacientes
        ]
        return JsonResponse(data, safe=False)
    if request.method == 'POST':
        if not request.user.has_perm('doctor.add_paciente'):
            return JsonResponse({'error': 'No autorizado'}, status=403)
        body = json.loads(request.body)
        p = Paciente.objects.create(
            nombres=body['nombre'],
            apellidos='',
            direccion=body['direccion'],
            telefono=body['telefono'],
            email=body['email'],
            fecha_nacimiento=datetime.now(),
            sexo='MASCULINO',
            estado_civil='SOLTERO',
            activo=True
        )
        return JsonResponse({'id': p.id, 'nombre': p.nombres, 'direccion': p.direccion, 'telefono': p.telefono, 'email': p.email})

@login_required
@permission_required('doctor.view_citamedica', raise_exception=True)
def api_citas(request):
    doctor_id = request.GET.get('doctor_id')
    year = request.GET.get('year')
    month = request.GET.get('month')
    # Solo doctores o asistentes pueden consultar
    if not (request.user.is_superuser or hasattr(request.user, 'doctor') or request.user.groups.filter(name='Asistentes').exists()):
        return JsonResponse({'error': 'No autorizado'}, status=403)
    if request.method == 'GET':
        # Si es doctor, solo sus citas
        if hasattr(request.user, 'doctor'):
            citas = CitaMedica.objects.filter(doctor=request.user.doctor, fecha__year=year, fecha__month=month)
        elif request.user.groups.filter(name='Asistentes').exists():
            citas = CitaMedica.objects.filter(fecha__year=year, fecha__month=month)
        else:
            citas = CitaMedica.objects.none()
        data = {}
        for c in citas:
            estado = 'ocupada' if c.estado == 'PENDIENTE' else 'atendida'
            data[str(c.fecha)] = {'estado': estado}
        return JsonResponse(data)
    if request.method == 'POST':
        body = json.loads(request.body)
        # Solo asistentes pueden crear citas para otros doctores
        if hasattr(request.user, 'doctor') and body.get('doctor') != request.user.doctor.id:
            return JsonResponse({'error': 'No puede agendar citas para otros doctores'}, status=403)
        # Validar doctor activo
        try:
            doctor = Doctor.objects.get(pk=body['doctor'], activo=True)
        except Doctor.DoesNotExist:
            return JsonResponse({'error': 'Doctor no activo o no existe'}, status=400)
        # Validar paciente activo
        try:
            paciente = Paciente.active_patient.get(pk=body['paciente'])
        except Paciente.DoesNotExist:
            return JsonResponse({'error': 'Paciente no activo o no existe'}, status=400)
        cita = CitaMedica.objects.create(
            paciente=paciente,
            doctor=doctor,
            fecha=body['fecha'],
            hora_cita=body['hora_cita'],
            estado='PENDIENTE',
            observaciones=body.get('observaciones', '')
        )
        return JsonResponse({'id': cita.id, 'fecha': cita.fecha, 'hora_cita': cita.hora_cita, 'estado': cita.estado})

@login_required
@permission_required('doctor.view_citamedica', raise_exception=True)
def api_horas_disponibles(request):
    """
    API para obtener las horas disponibles de un doctor en una fecha específica.
    Solo el doctor autenticado o asistentes pueden consultar.
    Parámetros GET:
        - fecha (YYYY-MM-DD)
        - doctor_id (opcional, solo asistentes)
    """
    import datetime
    if not (request.user.is_superuser or hasattr(request.user, 'doctor') or request.user.groups.filter(name='Asistentes').exists()):
        return JsonResponse({'error': 'No autorizado'}, status=403)
    fecha_str = request.GET.get('fecha')
    doctor_id = request.GET.get('doctor_id')
    if not fecha_str:
        return JsonResponse({'error': 'Debe proporcionar una fecha'}, status=400)
    try:
        fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except Exception:
        return JsonResponse({'error': 'Formato de fecha inválido'}, status=400)
    # Determinar el doctor
    if hasattr(request.user, 'doctor'):
        doctor = request.user.doctor
    elif request.user.groups.filter(name='Asistentes').exists() and doctor_id:
        try:
            doctor = Doctor.objects.get(pk=doctor_id, activo=True)
        except Doctor.DoesNotExist:
            return JsonResponse({'error': 'Doctor no encontrado o inactivo'}, status=404)
    else:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    # Obtener citas ocupadas
    citas_ocupadas = CitaMedica.objects.filter(doctor=doctor, fecha=fecha).values_list('hora_cita', flat=True)
    horas = obtener_horarios_disponibles_para_fecha(doctor, fecha, list(citas_ocupadas))
    data = [{'value': h.strftime('%H:%M'), 'label': h.strftime('%H:%M')} for h in horas]
    return JsonResponse({'horas': data})

