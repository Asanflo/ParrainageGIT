import json
from datetime import datetime
from flask_jwt_extended import get_jwt_identity

from extensions import db
from models import Surprise, Student

#====================================
# Serialisation de la surprise
#====================================
def surprise_to_dict(surprise):
    return {
        "id": surprise.id,
        "titre": surprise.titre,
        "type_media": surprise.type_media,
        "contenu": surprise.contenu,
        "mentor_id": surprise.mentor_id,
        "date_creation": surprise.date_creation
    }


#====================================
# CREATE Surprise
#====================================
def create_surprise(data):
    # Recuperer l'utilisateur courant
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)

    if not student:
        raise ValueError("Utilisateur introuvable")

    #  Vérifier le niveau
    if student.niveau != 4:
        raise PermissionError("Seuls les étudiants de niveau 4 peuvent créer une surprise")

    # Vérifier les champs obligatoires
    required_fields = ["titre", "type_media", "contenu"]
    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"Champ obligatoire manquant : {field}")

    # Creer la surprise
    surprise = Surprise(
        titre=data["titre"],
        type_media=data["type_media"],
        contenu=data["contenu"],
        mentor_id=student.id,
        date_creation=datetime.now()

    )
    db.session.add(surprise)
    db.session.commit()
    return surprise

# ====================================
# UPDATE SURPRISE - Service
# ====================================
def update_surprise(surprise, data, student):
    if student.niveau != 4:
        raise PermissionError("Seuls les étudiants de niveau 4 peuvent modifier une surprise")

    for field in ["titre", "type_media", "contenu"]:
        if field in data:
            setattr(surprise, field, data[field])

    db.session.commit()
    return surprise

