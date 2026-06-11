from app.database import db_cursor


def listar_especialidades():
    with db_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, nombre, descripcion
            FROM especialidades
            WHERE activo = 1
            ORDER BY nombre
            """
        )
        return cursor.fetchall()
