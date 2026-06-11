from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from app.models.cita_model import crear_cita, obtener_cita
from app.models.especialidad_model import listar_especialidades
from app.models.horario_model import listar_horarios_por_profesional, obtener_horario_disponible
from app.models.profesional_model import listar_profesionales_por_especialidad

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    return render_template("index.html")


@public_bp.route("/reservar")
def reservar():
    especialidades = listar_especialidades()
    return render_template("reservar.html", especialidades=especialidades)


@public_bp.route("/datos/profesionales/<int:especialidad_id>")
def datos_profesionales(especialidad_id):
    return jsonify(listar_profesionales_por_especialidad(especialidad_id))


@public_bp.route("/datos/horarios/<int:profesional_id>")
def datos_horarios(profesional_id):
    horarios = listar_horarios_por_profesional(profesional_id)
    serializados = []
    for horario in horarios:
        serializados.append({
            "id": horario["id"],
            "fecha": horario["fecha"].isoformat(),
            "hora_inicio": str(horario["hora_inicio"])[:5],
            "hora_fin": str(horario["hora_fin"])[:5],
            "disponible": bool(horario["disponible"]),
        })
    return jsonify(serializados)


@public_bp.route("/confirmar-cita", methods=["POST"])
def confirmar_cita():
    horario_id = request.form.get("horario_id", type=int)
    horario = obtener_horario_disponible(horario_id)

    if not horario:
        return redirect(url_for("public.reservar"))

    datos_paciente = {
        "nombre_completo": request.form.get("nombre_completo", "").strip(),
        "documento": request.form.get("documento", "").strip(),
        "telefono": request.form.get("telefono", "").strip(),
        "email": request.form.get("email", "").strip(),
        "fecha_nacimiento": request.form.get("fecha_nacimiento", "").strip(),
        "motivo": request.form.get("motivo", "").strip(),
    }

    if not datos_paciente["nombre_completo"] or not datos_paciente["telefono"] or not datos_paciente["email"]:
        return redirect(url_for("public.reservar"))

    cita_id = crear_cita(datos_paciente, horario)
    return redirect(url_for("public.confirmacion", cita_id=cita_id))


@public_bp.route("/confirmacion/<int:cita_id>")
def confirmacion(cita_id):
    cita = obtener_cita(cita_id)
    if not cita:
        return redirect(url_for("public.index"))
    return render_template("confirmacion.html", cita=cita)
