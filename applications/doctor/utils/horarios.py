from datetime import datetime, timedelta

def generar_horas_disponibles(horario, citas_ocupadas=None, intervalo_minutos=30):
    """
    Genera una lista de horas disponibles para agendar, omitiendo el intervalo bloqueado y las horas ocupadas.
    - horario: instancia de HorarioAtencion
    - citas_ocupadas: lista de horas (time) ya ocupadas
    - intervalo_minutos: minutos entre cada opción (ej. 30)
    """
    horas = []
    inicio = datetime.combine(datetime.today(), horario.hora_inicio)
    fin = datetime.combine(datetime.today(), horario.hora_fin)
    bloquea_desde = horario.intervalo_desde
    bloquea_hasta = horario.intervalo_hasta
    citas_ocupadas = citas_ocupadas or []

    actual = inicio
    while actual < fin:
        hora_actual = actual.time()
        # Omitir si está en el intervalo bloqueado
        if not (bloquea_desde and bloquea_hasta and bloquea_desde <= hora_actual < bloquea_hasta):
            # Omitir si ya está ocupada
            if hora_actual not in citas_ocupadas:
                horas.append(hora_actual)
        actual += timedelta(minutes=intervalo_minutos)
    return horas


def obtener_horarios_disponibles_para_fecha(doctor, fecha, citas_ocupadas=None, intervalo_minutos=30):
    """
    Devuelve la lista de horas disponibles para un doctor y una fecha específica,
    considerando el HorarioAtencion correspondiente al día de la semana.
    """
    dia_semana = fecha.strftime('%A').lower()  # Ej: 'monday', 'tuesday', etc.
    from applications.doctor.models import HorarioAtencion
    horario = HorarioAtencion.objects.filter(doctor=doctor, dia_semana=dia_semana, activo=True).first()
    if not horario:
        return []
    return generar_horas_disponibles(horario, citas_ocupadas, intervalo_minutos)
