import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy import func
from extensions import db
from models import Student
from werkzeug.security import generate_password_hash
import secrets


def import_students_from_excel(file_path):
    df = pd.read_excel(file_path)

    required_columns = ["Matricule", "Noms", "Filière", "Niveau"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Colonne manquante dans le fichier: {col}")

    created_students = []

    # Récupérer TOUS les matricules existants (1 seule requête)
    existing_matricules = {
        m.strip()
        for (m,) in db.session.query(Student.matricule).all()
    }

    students_to_add = []

    for _, row in df.iterrows():
        matricule = row.get("Matricule")

        if pd.isna(matricule) or str(matricule).strip() == "":
            continue

        matricule = str(matricule).strip()

        if matricule in existing_matricules:
            continue

        token_brut = secrets.token_urlsafe(8)

        student = Student(
            matricule=matricule,
            token=token_brut,
            password_hash=generate_password_hash(
                token_brut,
                method="pbkdf2:sha256"
            ),
            nom_complet=row["Noms"],
            niveau=int(row["Niveau"]),
            filiere=row["Filière"],
            telephone="",
            competences="[]",
            centres_interet="[]",
            reseaux_sociaux="{}",
        )

        students_to_add.append(student)
        existing_matricules.add(matricule)

    try:
        db.session.bulk_save_objects(students_to_add)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return {
        "created": len(students_to_add),
        "students": [s.matricule for s in students_to_add]
    }





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
