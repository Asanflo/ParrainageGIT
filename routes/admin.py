from flask import Blueprint, request, current_app, jsonify, send_file
import pandas as pd
from io import BytesIO

from models import Student
from scripts.import_student import import_students_from_excel

admin_bp = Blueprint("admin_bp", __name__)
EXCEL_FILE = "scripts/Liste_1.xlsx"

# ------------------------------
# SAVE students from excel file
# ------------------------------
@admin_bp.route("/import-students", methods=["POST"])
def import_students():
    system_key = request.headers.get("X-SYSTEM-KEY")

    if not system_key or system_key != current_app.config["SYSTEM_ASSIGN_KEY"]:
        return jsonify({"msg": "Unauthorized"}), 403

    try:
        created_students = import_students_from_excel(EXCEL_FILE)
        return jsonify({
            "message": f"{len(created_students)} étudiants créés",
            "students": created_students
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------
# IMPORT students to csv file
# ------------------------------
@admin_bp.route("/export-students", methods=["GET"])
def export_students_endpoint():
    filiere = request.args.get("filiere")
    niveau = request.args.get("niveau")
    system_key = request.headers.get("X-SYSTEM-KEY")

    if not system_key or system_key != current_app.config["SYSTEM_ASSIGN_KEY"]:
        return jsonify({"msg": "Unauthorized"}), 403

    if not filiere or not niveau:
        return {"error": "filiere et niveau requis"}, 400

    niveau = int(niveau)

    # ✅ Pas besoin de app.app_context(), Flask gère le contexte
    query = Student.query.filter_by(filiere=filiere, niveau=niveau)
    data = [{"matricule":s.matricule,"nom_complet": s.nom_complet, "token": s.token} for s in query.all()]

    if not data:
        return {"message": "Aucun étudiant trouvé"}, 404

    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"Etudiants_{filiere}_{niveau}.csv"
    )