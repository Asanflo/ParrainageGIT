import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from app import app, db
from models import Student

# Paramètres pour filtrer
FILIERE = "GLO"     # exemple : "INFO", "MATH", etc.
NIVEAU = 3       # exemple : 3,4, etc.

# Chemin du CSV de sortie
CSV_FILE = f"Etudiants_{FILIERE}_{NIVEAU}.csv"


def export_students(filiere, niveau, csv_file):
    with app.app_context():
        # Ici, j'assume que tu as des colonnes 'filiere' et 'salle' dans ton modèle Student
        query = Student.query.filter_by(filiere=filiere, niveau=niveau)

        data = []
        for student in query.all():
            data.append({
                "nom_complet": student.nom_complet,
                "token": student.token
            })

        if not data:
            print("Aucun étudiant trouvé pour ces critères")
            return

        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False)
        print(f"{len(data)} étudiants exportés dans {csv_file}")


if __name__ == "__main__":
    export_students(FILIERE, NIVEAU, CSV_FILE)
