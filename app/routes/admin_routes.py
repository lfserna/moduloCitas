from flask import Blueprint, render_template

from app.models.cita_model import listar_citas

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard")
def dashboard():
    citas = listar_citas()
    total_citas = len(citas)
    confirmadas = len([cita for cita in citas if cita["estado"] == "confirmada"])
    return render_template(
        "dashboard.html",
        citas=citas,
        total_citas=total_citas,
        confirmadas=confirmadas,
    )
