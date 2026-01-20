from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import os

from extensions import db
from models import Student, Surprise, SystemState
from services.mentor_service import assign_mentors_randomly
from services.surprise_service import surprise_to_dict
from services.student_service import student_to_dict

mentor_bp = Blueprint("mentor", __name__, url_prefix="/mentor")

# ------------------------------
# Afficher la liste des surprises d'un mentor donne
# ------------------------------
@mentor_bp.route("/<int:student_id>", methods=["GET"])
@jwt_required()
def list_mentor_surprises(student_id):
    """
    Récupère toutes les surprises créées par le mentor de l'étudiant donné.

    student_id : l'id du mentee connecté
    """
    # Récupérer l'étudiant (mentee)
    student = Student.query.get_or_404(student_id)

    # Vérifier que le mentee a bien un mentor assigné
    if not student.mentee_assignment:
        return jsonify({"msg": "Cet étudiant n'a pas de mentor assigné."}), 404

    mentor_id = student.mentee_assignment.mentor_id

    # Récupérer toutes les surprises du mentor
    surprises = Surprise.query.filter_by(mentor_id=mentor_id).all()
    surprises_dict = [surprise_to_dict(s) for s in surprises]

    return jsonify(surprises_dict), 200


# ------------------------------
# Route pour lancer l'assignation des parrains
# ------------------------------
@mentor_bp.route("/assign-mentors", methods=["POST"])
def assign_mentors_route():

    system_key = request.headers.get("X-SYSTEM-KEY")

    if not system_key or system_key != current_app.config["SYSTEM_ASSIGN_KEY"]:
        return jsonify({"msg": "Unauthorized"}), 403

    state = SystemState.query.first()

    if state and state.mentors_assigned:
        return jsonify({"msg": "Assignation déjà effectuée"}), 409

    # Lancer l’assignation
    assign_mentors_randomly(commit=True)

    if not state:
        state = SystemState()
        db.session.add(state)

    state.mentors_assigned = True
    state.executed_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"msg": "Assignation effectuée avec succès"}), 200

# ------------------------------
# Montrer le mentor ou le mentoree d'un etudiant
# ------------------------------
@mentor_bp.route("/relation", methods=["GET"])
@jwt_required()
def get_my_mentor_or_mentore():
    """
    Récupère le mentor ou le(s) mentorees de l'étudiant connecté.
    """
    student_id = get_jwt_identity()
    student = Student.query.get_or_404(student_id)

    # Si l'étudiant est un mentee
    if student.mentee_assignment:
        mentor = student.mentee_assignment.mentor
        return jsonify({
            "role": "mentee",
            "mentor": student_to_dict(mentor)
        }), 200

    # Si l'étudiant est un mentor
    if student.mentor_assignments:
        mentorees = [student_to_dict(m.mentee) for m in student.mentor_assignments]
        return jsonify({
            "role": "mentor",
            "mentorees": mentorees
        }), 200

    return jsonify({"msg": "Aucune relation mentor/mentoree trouvée"}), 404
