import json
from models import Student
from app import db
from datetime import datetime


# ------------------------------
# Sérialisation d'un student
# ------------------------------
def student_to_dict(student):
    return {
        "id": student.id,
        "matricule": student.matricule,
        "nom_complet": student.nom_complet,
        "niveau": student.niveau,
        "numero": student.numero,
        "competences": json.loads(student.competences) if student.competences else [],
        "centres_interet": json.loads(student.centres_interet) if student.centres_interet else [],
        "reseaux_sociaux": json.loads(student.reseaux_sociaux) if student.reseaux_sociaux else {},
        "photo_profil": student.photo_profil if hasattr(student, "photo_profil") else None,
        "created_at": student.created_at,
        "updated_at": student.updated_at
    }


# ------------------------------
# Créer un student (inscription)
# ------------------------------
def create_student(data):
    student = Student(
        matricule=data["matricule"],
        nom=data["nom_complet"],
        niveau=data["niveau"],
        numero=data.get("numero", ""),
        prenom=data.get("prenom"),  # nullable
        competences=json.dumps(data.get("competences", [])),
        centres_interet=json.dumps(data.get("centres_interet", [])),
        reseaux_sociaux=json.dumps(data.get("reseaux_sociaux", {})),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.session.add(student)
    db.session.commit()
    return student


# ------------------------------
# Mettre à jour un student
# ------------------------------
def update_student(student, data):
    # On ne modifie que les champs nullable
    if "numero" in data:
        student.numero = data["numero"]
    if "competences" in data:
        student.competences = json.dumps(data["competences"])
    if "centres_interet" in data:
        student.centres_interet = json.dumps(data["centres_interet"])
    if "reseaux_sociaux" in data:
        student.reseaux_sociaux = json.dumps(data["reseaux_sociaux"])
    if "photo_profil" in data:
        student.photo_profil = data["photo_profil"]

    student.updated_at = datetime.now()
    db.session.commit()
    return student

