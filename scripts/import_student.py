import sys
import os

from services.student_service import student_to_dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy import func
from extensions import db
from models import Student
from werkzeug.security import generate_password_hash
import secrets


def import_students_from_excel(file_path):
    df = pd.read_excel(file_path)

    created_students = []

    try:
        for _, row in df.iterrows():
            matricule = row.get("Matricule")

            if not matricule or pd.isna(matricule) or matricule.strip() == "":
                continue

            matricule = matricule.strip()

            if Student.query.filter_by(matricule=matricule).first():
                continue

            student = Student(
                matricule=matricule,
                token=secrets.token_urlsafe(8),
                password_hash=generate_password_hash(matricule),
                nom_complet=row["Noms"],
                niveau=int(row["Niveau"]),
                filiere=row["Filière"],
                competences="[]",
                centres_interet="[]",
                reseaux_sociaux="{}",
            )

            db.session.add(student)
            created_students.append(student_to_dict(student))

        # ✅ UN SEUL COMMIT
        # db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e

    return created_students






"""
def import_students_from_excel(file_path):
    df = pd.read_excel(file_path)

    required_columns = ["nom_complet", "matricule", "filiere", "niveau"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Colonne manquante dans le fichier: {col}")

    created_students = []
    with app.app_context():  # nécessaire pour utiliser SQLAlchemy
        for _, row in df.iterrows():
            if Student.query.filter_by(matricule=row["matricule"]).first():
                continue

            student_data = {
                "nom_complet": row["nom_complet"],
                "matricule": row["matricule"],
                "niveau": int(row["niveau"]),
                "filiere": row["filiere"],
                "telephone": row.get("telephone", ""),
                "competences": [],
                "centres_interet": [],
                "reseaux_sociaux": {},
            }
            student = create_student(student_data)
            created_students.append(student_to_dict(student))

    print(f"{len(created_students)} étudiants créés")
    for s in created_students:
        print(s)

    return created_students

"""
