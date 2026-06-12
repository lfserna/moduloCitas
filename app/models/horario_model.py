from datetime import date, datetime, timedelta
import unicodedata

from app.database import db_cursor


DIAS = {
    "lunes": 0,
    "martes": 1,
    "miercoles": 2,
    "jueves": 3,
    "viernes": 4,
    "sabado": 5,
    "domingo": 6,
}


def _normalizar(texto):
    texto = texto.lower().replace(" y ", ",")
    texto = unicodedata.normalize("NFD", texto)
    return "".join(caracter for caracter in texto if unicodedata.category(caracter) != "Mn")


def _dias_a_indices(dias_atencion):
    texto = _normalizar(dias_atencion)
    if "lunes a viernes" in texto:
        return {0, 1, 2, 3, 4}
    if "lunes a sabado" in texto:
        return {0, 1, 2, 3, 4, 5}
    indices = set()
    for nombre, indice in DIAS.items():
        if nombre in texto:
            indices.add(indice)
    return indices or {0, 1, 2, 3, 4}


def _a_datetime(fecha, hora):
    return datetime.combine(fecha, datetime.min.time()) + hora


def asegurar_horarios_desde_disponibilidad(profesional_id, dias=60):
    desde = date.today()
    hasta = desde + timedelta(days=dias)

    with db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            SELECT dias_atencion, hora_inicio, hora_fin, duracion_cita_minutos
            FROM disponibilidad_profesional
            WHERE profesional_id = %s AND activo = 1
            LIMIT 1
            """,
            (profesional_id,),
        )
        disponibilidad = cursor.fetchone()

        if not disponibilidad:
            return

        dias_validos = _dias_a_indices(disponibilidad["dias_atencion"])
        duracion = int(disponibilidad["duracion_cita_minutos"] or 30)
        fecha_actual = desde

        while fecha_actual <= hasta:
            if fecha_actual.weekday() in dias_validos:
                inicio = _a_datetime(fecha_actual, disponibilidad["hora_inicio"])
                fin_jornada = _a_datetime(fecha_actual, disponibilidad["hora_fin"])

                while inicio + timedelta(minutes=duracion) <= fin_jornada:
                    fin = inicio + timedelta(minutes=duracion)
                    cursor.execute(
                        """
                        INSERT IGNORE INTO horarios (profesional_id, fecha, hora_inicio, hora_fin, disponible)
                        VALUES (%s, %s, %s, %s, 1)
                        """,
                        (
                            profesional_id,
                            fecha_actual,
                            inicio.time(),
                            fin.time(),
                        ),
                    )
                    inicio = fin
            fecha_actual += timedelta(days=1)


def listar_horarios_por_profesional(profesional_id):
    asegurar_horarios_desde_disponibilidad(profesional_id)
    desde = date.today()
    hasta = desde + timedelta(days=60)

    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, fecha, hora_inicio, hora_fin, disponible
            FROM horarios
            WHERE profesional_id = %s
              AND fecha BETWEEN %s AND %s
            ORDER BY fecha, hora_inicio
            """,
            (profesional_id, desde, hasta),
        )
        return cursor.fetchall()


def obtener_horario_disponible(horario_id):
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT h.id, h.profesional_id, h.fecha, h.hora_inicio, h.hora_fin,
                   p.especialidad_id
            FROM horarios h
            INNER JOIN profesionales p ON p.id = h.profesional_id
            WHERE h.id = %s AND h.disponible = 1
            """,
            (horario_id,),
        )
        return cursor.fetchone()
