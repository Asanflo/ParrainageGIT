import random
from models import Student, MentorAssignment
from extensions import db
from collections import defaultdict

def assign_mentors_randomly(commit=True):
    """
        Assigne des mentors de niveau 4 à des mentorees de niveau 3
        par filière de manière aléatoire.
        Chaque mentor peut avoir au maximum 2 mentees.
    """
    mentors = Student.query.filter_by(niveau=4).all()
    mentorees = Student.query.filter_by(niveau=3).all()



    # Organiser mentors et mentees par filière
    mentors_by_filiere = defaultdict(list)
    mentorees_by_filiere = defaultdict(list)

    for m in mentors:
        mentors_by_filiere[m.filiere].append(m)
    for m in mentorees:
        mentorees_by_filiere[m.filiere].append(m)

    for filiere in mentors_by_filiere.keys():
        mentors_f = mentors_by_filiere[filiere]
        mentorees_f = mentorees_by_filiere.get(filiere, [])

        if not mentors_f or not mentorees_f:
            continue

        random.shuffle(mentors_f)
        random.shuffle(mentorees_f)

        # Compter combien de mentees chaque mentor a déjà
        mentee_count = {mentor.id: len(mentor.mentor_assignments) for mentor in mentors_f}

        # 1. Assigner 1 mentee à chaque mentor disponible
        for mentor, mentoree in zip(mentors_f, mentorees_f):
            if mentee_count[mentor.id] < 2:
                assignment = MentorAssignment(
                    mentor_id=mentor.id,
                    mentee_id=mentoree.id
                )
                db.session.add(assignment)
                mentee_count[mentor.id] += 1

        # 2. Redistribuer le reste en respectant la limite de 2 mentees par mentor
        remaining_mentees = mentorees_f[len(mentors_f):]
        for mentoree in remaining_mentees:
            # choisir un mentor qui n'a pas encore 2 mentees
            available_mentors = [m for m in mentors_f if mentee_count[m.id] < 2]
            if not available_mentors:
                break  # plus de mentor disponible
            mentor = random.choice(available_mentors)
            assignment = MentorAssignment(
                mentor_id=mentor.id,
                mentee_id=mentoree.id
            )
            db.session.add(assignment)
            mentee_count[mentor.id] += 1

    if commit:
        db.session.commit()

    return True



# def assign_mentors_randomly():
#     """
#     Assigne des mentors de niveau 4 à des mentorees de niveau 3
#     par filière de manière aléatoire.
#     """
#     # Récupérer tous les mentors et mentorees
#     mentors = Student.query.filter_by(niveau=4).all()
#     mentorees = Student.query.filter_by(niveau=3).all()
#
#     # Grouper les mentors et mentorees par filière
#     filieres = set([s.filiere for s in mentors + mentorees])
#
#     for filiere in filieres:
#         # Mentors et mentorees dans cette filière
#         mentors_f = [m for m in mentors if m.filiere == filiere]
#         mentorees_f = [m for m in mentorees if m.filiere == filiere]
#
#         if not mentors_f or not mentorees_f:
#             continue  # rien à assigner
#
#         # Etape 1 : assigner un seul mentoree par mentor (non assigné)
#         unassigned_mentorees = [
#             m for m in mentorees_f
#             if not MentorAssignment.query.filter_by(mentee_id=m.id).first()
#         ]
#         random.shuffle(unassigned_mentorees)
#         random.shuffle(mentors_f)
#
#         # Assignation initiale
#         for mentor, mentoree in zip(mentors_f, unassigned_mentorees):
#             assignment = MentorAssignment(
#                 mentor_id=mentor.id,
#                 mentee_id=mentoree.id
#             )
#             db.session.add(assignment)
#
#         db.session.commit()
#
#         # Etape 2 : redistribution pour mentorees restantes
#         remaining_mentorees = [
#             m for m in mentorees_f
#             if not MentorAssignment.query.filter_by(mentee_id=m.id).first()
#         ]
#         if remaining_mentorees:
#             for mentoree in remaining_mentorees:
#                 mentor = random.choice(mentors_f)
#                 assignment = MentorAssignment(
#                     mentor_id=mentor.id,
#                     mentee_id=mentoree.id
#                 )
#                 db.session.add(assignment)
#             db.session.commit()
#
#     return True
