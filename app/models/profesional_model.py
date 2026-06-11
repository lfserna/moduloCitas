from app.database import db_cursor


def listar_profesionales_por_especialidad(especialidad_id):
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, nombre, matricula, foto_url, descripcion
            FROM profesionales
            WHERE especialidad_id = %s AND activo = 1
            ORDER BY nombre
            """,
            (especialidad_id,),
        )
        return cursor.fetchall()
