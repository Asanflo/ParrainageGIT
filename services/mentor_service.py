import random
from models import Student, MentorAssignment
from extensions import db


def assign_mentors_randomly():
    """
    Assigne des mentors de niveau 4 à des mentorees de niveau 3
    par filière de manière aléatoire.
    """
    # Récupérer tous les mentors et mentorees
    mentors = Student.query.filter_by(niveau=4).all()
    mentorees = Student.query.filter_by(niveau=3).all()

    # Grouper les mentors et mentorees par filière
    filieres = set([s.filiere for s in mentors + mentorees])

    for filiere in filieres:
        # Mentors et mentorees dans cette filière
        mentors_f = [m for m in mentors if m.filiere == filiere]
        mentorees_f = [m for m in mentorees if m.filiere == filiere]

        if not mentors_f or not mentorees_f:
            continue  # rien à assigner

        # Etape 1 : assigner un seul mentoree par mentor (non assigné)
        unassigned_mentorees = [
            m for m in mentorees_f
            if not MentorAssignment.query.filter_by(mentee_id=m.id).first()
        ]
        random.shuffle(unassigned_mentorees)
        random.shuffle(mentors_f)

        # Assignation initiale
        for mentor, mentoree in zip(mentors_f, unassigned_mentorees):
            assignment = MentorAssignment(
                mentor_id=mentor.id,
                mentee_id=mentoree.id
            )
            db.session.add(assignment)

        db.session.commit()

        # Etape 2 : redistribution pour mentorees restantes
        remaining_mentorees = [
            m for m in mentorees_f
            if not MentorAssignment.query.filter_by(mentee_id=m.id).first()
        ]
        if remaining_mentorees:
            for mentoree in remaining_mentorees:
                mentor = random.choice(mentors_f)
                assignment = MentorAssignment(
                    mentor_id=mentor.id,
                    mentee_id=mentoree.id
                )
                db.session.add(assignment)
            db.session.commit()

    return True
