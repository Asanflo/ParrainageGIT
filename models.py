from extensions import db
from datetime import datetime
import json


#Definition of models

#Classe Etudiant
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(15), unique=True, nullable=False)
    token = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nom_complet = db.Column(db.String(255), nullable=False)

    niveau = db.Column(db.Integer, nullable=False)
    filiere = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(20), nullable=True)

    competences = db.Column(db.Text) #JSON ou liste de competences sous forne de texte
    centres_interet = db.Column(db.Text)
    reseaux_sociaux = db.Column(db.Text)


    photo_profil = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    #Relations
    mentor_assignments = db.relationship(
        "MentorAssignment",
        back_populates="mentor",
        foreign_keys="MentorAssignment.mentor_id"
    )

    mentee_assignment = db.relationship(
        "MentorAssignment",
        back_populates="mentee",
        uselist=False,
        foreign_keys="MentorAssignment.mentee_id"
    )

    surprises = db.relationship(
        "Surprise",
        back_populates="mentor",
        cascade="all, delete-orphan"
    )

    #Fonction de traitement des donnees
    def get_competences(self):
        try:
            return json.loads(self.competences)
        except Exception:
            return []

    def get_centres_interet(self):
        try:
            return json.loads(self.centres_interet)
        except Exception:
            return []

    def get_reseaux_sociaux(self):
        try:
            return json.loads(self.reseaux_sociaux)
        except Exception:
            return {}

    def get_whatsapp_link(self):
        if not self.telephone:
            return None
        return f"https://wa.me/{self.telephone}"

#Classe Assignation mentor
class MentorAssignment(db.Model):
    __tablename__ = 'mentor_assignments'
    id = db.Column(db.Integer, primary_key=True)

    mentor_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id'),
        nullable = False
    )

    mentee_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id'),
        nullable = False
    )

    date_attribution = db.Column(db.DateTime, default=datetime.utcnow())
    statut = db.Column(
        db.String(20),
        default="actif"
    )

    #Relations
    # Relations
    mentor = db.relationship(
        "Student",
        back_populates="mentor_assignments",
        foreign_keys=[mentor_id]
    )

    mentee = db.relationship(
        "Student",
        back_populates="mentee_assignment",
        foreign_keys=[mentee_id]
    )

#Classe suprise
class Surprise(db.Model):
    __tablename__ = "surprises"

    id = db.Column(db.Integer, primary_key=True)

    titre = db.Column(db.String(100), nullable=False)

    type_media = db.Column(
        db.String(20),
        nullable=False
    )
    # TEXTE, GIF, IMAGE, VIDEO, LIEN, AUDIO, DEFI

    contenu = db.Column(
        db.Text,
        nullable=False
    )

    mentor_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    mentor = db.relationship(
        "Student",
        back_populates="surprises"
    )