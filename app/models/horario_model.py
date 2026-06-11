from app.database import db_cursor


def listar_horarios_por_profesional(profesional_id):
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, fecha, hora_inicio, hora_fin, disponible
            FROM horarios
            WHERE profesional_id = %s
            ORDER BY fecha, hora_inicio
            """,
            (profesional_id,),
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
