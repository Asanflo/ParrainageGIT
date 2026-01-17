import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from app import app
from extensions import db
from models import Student
from services.student_service import create_student, student_to_dict


# Chemin vers ton fichier Excel
EXCEL_FILE = "scripts/x.xlsx"

def import_students_from_excel(file_path):
    df = pd.read_excel(file_path)

    required_columns = ["nom_complet", "matricule", "filiere", "niveau"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Colonne manquante dans le fichier: {col}")

    created_students = []
    with app.app_context():  # nécessaire pour utiliser SQLAlchemy
        for _, row in df.iterrows():
            # Vérifie si le matricule existe déjà
            if Student.query.filter_by(matricule=row["matricule"]).first():
                continue  # ignore les doublons

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

if __name__ == "__main__":
    import_students_from_excel(EXCEL_FILE)
