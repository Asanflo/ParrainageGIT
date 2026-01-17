from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
from models import Student
from services.student_service import student_to_dict, create_student, update_student, delete_student

student_bp = Blueprint("student", __name__, url_prefix="/api/student")

# ------------------------------
# CREATE student
# ------------------------------
@student_bp.route("/", methods=["POST"])
def register_student():
    """
    Documentation de l'endpoint POST- http://127.0.0.1:5000/api/student/
    Structure des donnees a envoyer
    {
      "matricule": "24IN01",
      "nom_complet": "Jean Dupo",
      "niveau": 3,
      "filiere": "GLO",
      "telephone": "699123456",
      "competences": ["Python", "Flask", "SQL"],
      "centres_interet": ["Backend", "Sécurité"],
      "reseaux_sociaux": {
        "linkedin": "https://linkedin.com/in/jeandupont",
        "github": "https://github.com/jeandupont"
      }
    }

    Message recus:
    OK-statut: 201

    {
        "msg": "Student créé",
        "student": {
            "centres_interet": [
                "Backend",
                "Sécurité"
            ],
            "competences": [
                "Python",
                "Flask",
                "SQL"
            ],
            "created_at": "Sat, 17 Jan 2026 11:56:38 GMT",
            "filiere": "GLO",
            "id": 13,
            "matricule": "24IN01",
            "niveau": 3,
            "nom_complet": "Jean Dupo",
            "photo_profil": null,
            "reseaux_sociaux": {
                "github": "https://github.com/jeandupont",
                "linkedin": "https://linkedin.com/in/jeandupont"
            },
            "telephone": "699123456",
            "updated_at": "Sat, 17 Jan 2026 11:56:38 GMT"
        }
    }

    """
    data = request.get_json()
    # Vérifier les champs obligatoires
    if not data.get("matricule") or not data.get("nom_complet") or not data.get("niveau"):
        return jsonify({"msg": "matricule, nom et niveau requis"}), 400
    if Student.query.filter_by(matricule=data["matricule"]).first():
        return jsonify({"msg": "matricule déjà existant"}), 400

    student = create_student(data)
    return jsonify({"msg": "Student créé", "student": student_to_dict(student)}), 201


# ------------------------------
# GET current logged-in student
# ------------------------------
@student_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_student():
    """
    Récupère les informations de l’étudiant actuellement connecté via JWT.

    ---
    tags:
      - Students
    security:
      - bearerAuth: []
    responses:
      200:
        description: Informations de l’étudiant
        content:
          application/json:
            example:
              student:
                id: 1
                matricule: "2026A001"
                token: "abcd1234"
                nom_complet: "Florentin Agassem"
                niveau: 3
                filiere: "Informatique"
                telephone: "+237690000000"
                competences: ["Python", "SQL"]
                centres_interet: ["AI", "Web"]
                reseaux_sociaux: {"linkedin": "https://linkedin.com/in/florentin"}
                photo_profil: null
                created_at: "2026-01-17T10:00:00"
                updated_at: "2026-01-17T10:00:00"
      401:
        description: JWT manquant ou invalide
    """
    # Récupère l'ID du JWT
    current_user_id = get_jwt_identity()
    # Cherche l'utilisateur dans la DB
    student = Student.query.get_or_404(current_user_id)
    # Retourne ses infos
    return jsonify({"student": student_to_dict(student)})

# ------------------------------
# UPDATE student
# ------------------------------
@student_bp.route("/<int:student_id>", methods=["PUT"])
@jwt_required()
def modify_student(student_id):
    """
        Met à jour certaines informations de l’étudiant (telephone, photo, compétences, centres d’intérêt, réseaux sociaux).

        ---
        tags:
          - Students
        security:
          - bearerAuth: []
        parameters:
          - name: student_id
            in: path
            description: ID de l’étudiant
            required: true
            schema:
              type: integer
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  telephone:
                    type: string
                    example: "+237690000001"
                  photo_profil:
                    type: string
                    example: "https://example.com/photo.jpg"
                  competences:
                    type: array
                    items:
                      type: string
                    example: ["Python", "Django"]
                  centres_interet:
                    type: array
                    items:
                      type: string
                    example: ["Web", "Blockchain"]
                  reseaux_sociaux:
                    type: object
                    example: {"linkedin": "https://linkedin.com/in/florentin"}
        responses:
          200:
            description: Étudiant mis à jour avec succès
            content:
              application/json:
                example:
                  msg: "Student mis à jour"
                  student:
                    id: 1
                    matricule: "2026A001"
                    token: "abcd1234"
                    nom_complet: "Florentin Agassem"
                    niveau: 3
                    filiere: "Informatique"
                    telephone: "+237690000001"
                    competences: ["Python", "Django"]
                    centres_interet: ["Web", "Blockchain"]
                    reseaux_sociaux: {"linkedin": "https://linkedin.com/in/florentin"}
                    photo_profil: "https://example.com/photo.jpg"
                    created_at: "2026-01-17T10:00:00"
                    updated_at: "2026-01-17T12:00:00"
          404:
            description: Étudiant non trouvé
    """
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    student = update_student(student, data)
    return jsonify({"msg": "Student mis à jour", "student": student_to_dict(student)})

# ------------------------------
# DELETE student
# ------------------------------
@student_bp.route("/<int:student_id>", methods=["DELETE"])
@jwt_required()
def delete_student_route(student_id):
    """
        Supprime un étudiant de la base de données.

        ---
        tags:
          - Students
        security:
          - bearerAuth: []
        parameters:
          - name: student_id
            in: path
            description: ID de l’étudiant à supprimer
            required: true
            schema:
              type: integer
        responses:
          200:
            description: Étudiant supprimé avec succès
            content:
              application/json:
                example:
                  msg: "Student supprimé"
          404:
            description: Étudiant non trouvé
    """
    student = Student.query.get_or_404(student_id)
    delete_student(student)

    return jsonify({"msg": "Student supprimé"}), 200

# ------------------------------
# LIST all students
# ------------------------------
@student_bp.route("/", methods=["GET"])
@jwt_required()
def list_students():
    """
        Retourne la liste complète des étudiants.

        ---
        tags:
          - Students
        security:
          - bearerAuth: []
        responses:
          200:
            description: Liste des étudiants
            content:
              application/json:
                example:
                  - id: 1
                    matricule: "2026A001"
                    nom_complet: "Florentin Agassem"
                    niveau: 3
                    filiere: "Informatique"
                    telephone: "+237690000000"
                    competences: ["Python", "SQL"]
                    centres_interet: ["AI", "Web"]
                    reseaux_sociaux: {"linkedin": "https://linkedin.com/in/florentin"}
                    photo_profil: null
                    created_at: "2026-01-17T10:00:00"
                    updated_at: "2026-01-17T10:00:00"

         """
    students = Student.query.all()
    return jsonify([student_to_dict(s) for s in students])

