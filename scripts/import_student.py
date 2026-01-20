import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from extensions import db
from models import Student
from services.student_service import create_student, student_to_dict

#Script permettant d'ajouter atomatiquement les etudiants
def import_students_from_excel(file_path):
    df = pd.read_excel(file_path)

    required_columns = ["Matricule", "Noms", "Filière", "Niveau"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Colonne manquante dans le fichier: {col}")

    created_students = []

    # Trouver le dernier numéro existant dans la base
    last_student = Student.query.order_by(Student.id.desc()).first()
    if last_student and last_student.matricule.startswith("26PG"):
        last_num = int(last_student.matricule[-4:])
    else:
        last_num = 0

    for _, row in df.iterrows():
        matricule = row.get("Matricule")

        if not matricule or pd.isna(matricule) or matricule.strip() == "":
            last_num += 1
            matricule = f"26PG{last_num:04d}"

        if Student.query.filter_by(matricule=matricule).first():
            continue

        student_data = {
            "nom_complet": row["Noms"],
            "matricule": matricule,
            "niveau": int(row["Niveau"]),
            "filiere": row["Filière"],
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
