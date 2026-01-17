from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required,get_jwt_identity
from models import Student


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    """
        Connexion d'un étudiant avec matricule et mot de passe.

        ---
        tags:
          - Auth
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - matricule
                  - password
                properties:
                  matricule:
                    type: string
                    example: "2026A001"
                  password:
                    type: string
                    format: password
                    example: "motdepasse123"
        responses:
          200:
            description: Authentification réussie, tokens générés
            content:
              application/json:
                example:
                  access_token: "eyJ0eXAiOiJKV1QiLCJh..."
                  refresh_token: "eyJ0eXAiOiJKV1QiLCJh..."
                  student_name: "Florentin Agassem"
          401:
            description: Identifiants invalides
            content:
              application/json:
                example:
                  msg: "Identifiants invalides"
    """
    data = request.get_json()
    matricule = data.get("matricule")
    password = data.get("password")

    # Vérifier si l'utilisateur existe
    user = Student.query.filter_by(matricule=matricule).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"msg": "Identifiants invalides"}), 401


    # Générer tokens
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "student_name": user.nom_complet,
    })

#Endpoint pour le refresh token
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
        Rafraîchit le token d'accès à partir d'un refresh token valide.

        ---
        tags:
          - Auth
        security:
          - bearerAuth: []
        responses:
          200:
            description: Nouveau token d'accès généré
            content:
              application/json:
                example:
                  access_token: "eyJ0eXAiOiJKV1QiLCJh..."
          401:
            description: Refresh token invalide ou expiré
            content:
              application/json:
                example:
                  msg: "Token invalide ou expiré"
    """
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)

    return jsonify({"access_token": new_access_token}), 200

