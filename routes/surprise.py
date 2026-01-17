from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Student, Surprise
from services.surprise_service import create_surprise, surprise_to_dict, update_surprise

surprise_bp = Blueprint("surprise", __name__, url_prefix="/api/surprises")

# ------------------------------
# CREATE surprise
# ------------------------------
@surprise_bp.route("/", methods=["POST"])
@jwt_required()
def create_surprise_route():
    """
        Crée une nouvelle surprise pour l'étudiant connecté.

        Header requis:
            Authorization: Bearer <JWT_token>

        JSON attendu (Content-Type: application/json):
        {
            "titre": "Titre de la surprise",
            "type_media": "TEXTE | GIF | IMAGE | VIDEO | LIEN | AUDIO | DEFI",
            "contenu": "Texte ou URL du média"
        }

        Conditions:
            - L'étudiant connecté doit être de niveau 4.

        Réponses possibles:
            201 Created:
                {
                    "msg": "Surprise créée",
                    "surprise": {
                        "id": 1,
                        "titre": "Titre de la surprise",
                        "type_media": "TEXTE",
                        "contenu": "Contenu de la surprise",
                        "mentor_id": 42,
                        "date_creation": "2026-01-17T13:00:00"
                    }
                }
            403 Forbidden:
                {
                    "msg": "Seuls les étudiants de niveau 4 peuvent créer des surprises."
                }
            400 Bad Request:
                {
                    "msg": "Le champ 'titre' est obligatoire."
                }
        """
    data = request.get_json()

    try:
        surprise = create_surprise(data)
        return jsonify({
            "msg": "Surprise créée avec succès",
            "surprise": surprise_to_dict(surprise)
        }), 201

    except PermissionError as e:
        return jsonify({"msg": str(e)}), 403

    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

# ------------------------------
# UPDATE surprise
# ------------------------------
@surprise_bp.route("/<int:surprise_id>", methods=["PUT"])
@jwt_required()
def update_surprise_route(surprise_id):
    """
    Met à jour une surprise existante. Seuls les étudiants de niveau 4 peuvent effectuer cette action.

    Header requis:
        Authorization: Bearer <JWT_token>

    JSON attendu (Content-Type: application/json):
    {
        "titre": "Nouveau titre",
        "type_media": "TEXTE | GIF | IMAGE | VIDEO | LIEN | AUDIO | DEFI",
        "contenu": "Nouveau contenu"
    }
    """


    student_id = get_jwt_identity()
    student = Student.query.get_or_404(student_id)
    surprise = Surprise.query.get_or_404(surprise_id)

    data = request.get_json()

    try:
        surprise = update_surprise(surprise, data, student)
    except PermissionError as e:
        return jsonify({"msg": str(e)}), 403

    return jsonify({"msg": "Surprise mise à jour", "surprise": surprise_to_dict(surprise)}), 200

# ------------------------------
# LIST surprise
# ------------------------------
@surprise_bp.route("/", methods=["GET"])
@jwt_required()
def list_my_surprises():
    """
    Récupère toutes les surprises de l'utilisateur connecté.

    Header requis:
        Authorization: Bearer <JWT_token>

    Retour:
        JSON listant toutes les surprises de l'étudiant
    """

    student_id = get_jwt_identity()
    student = Student.query.get_or_404(student_id)

    # On utilise la relation back_populates définie dans le modèle Student
    surprises = [surprise_to_dict(s) for s in student.surprises]

    return jsonify(surprises), 200