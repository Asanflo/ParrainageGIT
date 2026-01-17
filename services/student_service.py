import json
import secrets
from datetime import datetime
from werkzeug.security import generate_password_hash
from extensions import db
from models import Student

# ------------------------------
# Sérialisation d'un student
# ------------------------------
def student_to_dict(student):
    return {
        "id": student.id,
        "matricule": student.matricule,
        "nom_complet": student.nom_complet,
        "niveau": student.niveau,
        "filiere": student.filiere,
        "telephone": student.telephone,
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
    token_brut = secrets.token_urlsafe(8)
    student = Student(
        matricule=data["matricule"],
        token=token_brut,
        password_hash=generate_password_hash(token_brut),
        nom_complet=data["nom_complet"],
        niveau=data["niveau"],
        filiere=data["filiere"],
        telephone=data.get("telephone", ""),
        competences=json.dumps(data.get("competences", [])),
        centres_interet=json.dumps(data.get("centres_interet", [])),
        reseaux_sociaux=json.dumps(data.get("reseaux_sociaux", {})),
    )
    db.session.add(student)
    db.session.commit()
    return student

# ------------------------------
# UPDATE un student
# ------------------------------
def update_student(student, data):
    print("update_student data:", data)
    for field in ["telephone", "photo_profil"]:
        if field in data:
            setattr(student, field, data[field])

    for field in ["competences", "centres_interet", "reseaux_sociaux"]:
        if field in data:
            setattr(student, field, json.dumps(data[field]))

    db.session.commit()
    return student

# ------------------------------
# DELETE un student
# ------------------------------
def delete_student(student):
    db.session.delete(student)
    db.session.commit()
