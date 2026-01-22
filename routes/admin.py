from flask import Blueprint, request, current_app, jsonify, send_file
import pandas as pd
from io import BytesIO

from models import Student
from scripts.import_student import import_students_from_excel

admin_bp = Blueprint("admin_bp", __name__)
EXCEL_FILE = "scripts/List_2.xlsx"

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


@admin_bp.route("/etudiants", methods=["GET"])
def list_students():
    """
    Lister tous les étudiants avec pagination

    Query params:
    - page: numéro de page (défaut: 1)
    - per_page: étudiants par page (défaut: 50, max: 200)
    - filiere: filtrer par filière
    - niveau: filtrer par niveau
    - search: rechercher dans nom ou matricule
    """
    system_key = request.headers.get("X-SYSTEM-KEY")

    if not system_key or system_key != current_app.config["SYSTEM_ASSIGN_KEY"]:
        return jsonify({"msg": "Unauthorized"}), 403

    try:
        # Paramètres de pagination
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 50, type=int), 200)

        # Filtres
        filiere = request.args.get('filiere')
        niveau = request.args.get('niveau', type=int)

        # Construire la requête
        query = Student.query

        if filiere:
            query = query.filter(Student.filiere == filiere)

        if niveau:
            query = query.filter(Student.niveau == niveau)

        # Paginer
        pagination = query.order_by(Student.id.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        students = [
            {
                "id": s.id,
                "nom_complet": s.nom_complet,
                "matricule": s.matricule,
                "filiere": s.filiere,
                "niveau": s.niveau,
                "telephone": s.telephone,
            }
            for s in pagination.items
        ]

        return jsonify({
            "students": students,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500