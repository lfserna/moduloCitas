from app.database import db_cursor


def crear_cita(datos_paciente, horario):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO pacientes (nombre_completo, documento, telefono, email, fecha_nacimiento)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                datos_paciente["nombre_completo"],
                datos_paciente.get("documento"),
                datos_paciente["telefono"],
                datos_paciente["email"],
                datos_paciente.get("fecha_nacimiento") or None,
            ),
        )
        paciente_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO citas (paciente_id, especialidad_id, profesional_id, horario_id, motivo, estado)
            VALUES (%s, %s, %s, %s, %s, 'confirmada')
            """,
            (
                paciente_id,
                horario["especialidad_id"],
                horario["profesional_id"],
                horario["id"],
                datos_paciente.get("motivo"),
            ),
        )
        cita_id = cursor.lastrowid

        cursor.execute(
            """
            UPDATE horarios
            SET disponible = 0
            WHERE id = %s AND disponible = 1
            """,
            (horario["id"],),
        )

        return cita_id


def listar_citas():
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT c.id, c.estado, c.motivo, c.creado_en,
                   pa.nombre_completo AS paciente, pa.telefono, pa.email,
                   e.nombre AS especialidad,
                   pr.nombre AS profesional,
                   h.fecha, h.hora_inicio, h.hora_fin
            FROM citas c
            INNER JOIN pacientes pa ON pa.id = c.paciente_id
            INNER JOIN especialidades e ON e.id = c.especialidad_id
            INNER JOIN profesionales pr ON pr.id = c.profesional_id
            INNER JOIN horarios h ON h.id = c.horario_id
            ORDER BY h.fecha DESC, h.hora_inicio DESC
            """
        )
        return cursor.fetchall()


def obtener_cita(cita_id):
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT c.id, c.estado, c.motivo,
                   pa.nombre_completo AS paciente, pa.telefono, pa.email,
                   e.nombre AS especialidad,
                   pr.nombre AS profesional,
                   h.fecha, h.hora_inicio, h.hora_fin
            FROM citas c
            INNER JOIN pacientes pa ON pa.id = c.paciente_id
            INNER JOIN especialidades e ON e.id = c.especialidad_id
            INNER JOIN profesionales pr ON pr.id = c.profesional_id
            INNER JOIN horarios h ON h.id = c.horario_id
            WHERE c.id = %s
            """,
            (cita_id,),
        )
        return cursor.fetchone()
