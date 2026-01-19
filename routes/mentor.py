from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from models import Student, Surprise
from services.surprise_service import surprise_to_dict

mentor_bp = Blueprint("mentor", __name__, url_prefix="/mentor")

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