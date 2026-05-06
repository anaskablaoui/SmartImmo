import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, 'SmartiImmo')
sys.path.append(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartiImmo.settings')

import django

django.setup()

from datetime import date
from django.db import transaction
from django.db.utils import IntegrityError
from accounts.models import CustomUser
from Administrateur.models import Administrateur
from Agents.models import Agents, Baux, Contrat, Offre
from Proprietaire.models import Proprietaire, Propriete
from Locataire.models import Locataire, Maintenance, demandeLocation


def get_or_create_user(email, password, role, nom, prenom, extra_fields=None):
    extra_fields = extra_fields or {}
    user = CustomUser.objects.filter(email=email).first()
    if user:
        print(f"Utilisateur existant trouvé : {email}")
        return user

    if role == 'administrateur':
        user = CustomUser.objects.create_superuser(
            email=email,
            password=password,
            nom=nom,
            prenom=prenom,
            role=role,
        )
    else:
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            nom=nom,
            prenom=prenom,
            role=role,
            **extra_fields,
        )

    print(f"Utilisateur créé : {email} ({role})")
    return user


def create_role_profile(role, email, password, nom, prenom, defaults):
    user = get_or_create_user(email=email, password=password, role=role, nom=nom, prenom=prenom)
    if role == 'administrateur':
        profile_obj, _ = Administrateur.objects.update_or_create(user=user, defaults=defaults)
    elif role == 'agent':
        profile_obj, _ = Agents.objects.update_or_create(user=user, defaults=defaults)
    elif role == 'proprietaire':
        profile_obj, _ = Proprietaire.objects.update_or_create(user=user, defaults=defaults)
    elif role == 'locataire':
        profile_obj, _ = Locataire.objects.update_or_create(user=user, defaults=defaults)
    else:
        profile_obj = None
    return user, profile_obj


def create_profiles():
    with transaction.atomic():
        admin_user, admin_obj = create_role_profile(
            role='administrateur',
            email='anas.kablaoui@gmail.com',
            password='anas123',
            nom='Anas',
            prenom='Kablaoui',
            defaults={'matricule': 'ADM001'},
        )

        agent_user, agent_obj = create_role_profile(
            role='agent',
            email='agent@gmail.com',
            password='agent123',
            nom='Agent',
            prenom='Example',
            defaults={'matricule': 'AG001', 'cin': '1234567890', 'telephone': '0612345678'},
        )

        proprietaire_user, proprietaire_obj = create_role_profile(
            role='proprietaire',
            email='prop@gmail.com',
            password='prop@gmail.com',
            nom='Prop',
            prenom='Example',
            defaults={'cin': '0987654321', 'telephone': '0712345678'},
        )

        locataire_user, locataire_obj = create_role_profile(
            role='locataire',
            email='client@gmail.com',
            password='client123',
            nom='Client',
            prenom='Example',
            defaults={'cin': '1122334455', 'telephone': '0723456789'},
        )

        extra_agents = [
            {'email': 'agent1@gmail.com', 'password': 'agent123', 'nom': 'Youssef', 'prenom': 'El Idrissi', 'matricule': 'AG002', 'cin': '2234567890', 'telephone': '0612345679'},
            {'email': 'agent2@gmail.com', 'password': 'agent123', 'nom': 'Leila', 'prenom': 'Naimi', 'matricule': 'AG003', 'cin': '3234567890', 'telephone': '0612345680'},
        ]
        extra_proprietaires = [
            {'email': 'prop1@gmail.com', 'password': 'prop123', 'nom': 'Karim', 'prenom': 'Benz', 'cin': '1987654321', 'telephone': '0712345679'},
            {'email': 'prop2@gmail.com', 'password': 'prop123', 'nom': 'Nadia', 'prenom': 'Sahraoui', 'cin': '2987654321', 'telephone': '0712345680'},
            {'email': 'prop3@gmail.com', 'password': 'prop123', 'nom': 'Rachid', 'prenom': 'Amrani', 'cin': '3987654321', 'telephone': '0712345681'},
        ]
        extra_locataires = [
            {'email': 'client1@gmail.com', 'password': 'client123', 'nom': 'Sara', 'prenom': 'Mansouri', 'cin': '2122334455', 'telephone': '0723456790'},
            {'email': 'client2@gmail.com', 'password': 'client123', 'nom': 'Hassan', 'prenom': 'Fassi', 'cin': '3122334455', 'telephone': '0723456791'},
            {'email': 'client3@gmail.com', 'password': 'client123', 'nom': 'Meryem', 'prenom': 'Jad', 'cin': '4122334455', 'telephone': '0723456792'},
            {'email': 'client4@gmail.com', 'password': 'client123', 'nom': 'Omar', 'prenom': 'Khalfi', 'cin': '5122334455', 'telephone': '0723456793'},
        ]

        agent_objs = [agent_obj]
        for entry in extra_agents:
            _, extra_agent = create_role_profile(
                role='agent',
                email=entry['email'],
                password=entry['password'],
                nom=entry['nom'],
                prenom=entry['prenom'],
                defaults={'matricule': entry['matricule'], 'cin': entry['cin'], 'telephone': entry['telephone']},
            )
            agent_objs.append(extra_agent)

        proprietaire_objs = [proprietaire_obj]
        for entry in extra_proprietaires:
            _, extra_prop = create_role_profile(
                role='proprietaire',
                email=entry['email'],
                password=entry['password'],
                nom=entry['nom'],
                prenom=entry['prenom'],
                defaults={'cin': entry['cin'], 'telephone': entry['telephone']},
            )
            proprietaire_objs.append(extra_prop)

        locataire_objs = [locataire_obj]
        for entry in extra_locataires:
            _, extra_loc = create_role_profile(
                role='locataire',
                email=entry['email'],
                password=entry['password'],
                nom=entry['nom'],
                prenom=entry['prenom'],
                defaults={'cin': entry['cin'], 'telephone': entry['telephone']},
            )
            locataire_objs.append(extra_loc)

        propriete_list = [
            {'adresse': '15 rue des Fleurs, Casablanca', 'nom': 'Appartement Fleurs', 'ville': 'Casablanca', 'etat': 'Disponible', 'metrage': 85.0, 'proprietaire': proprietaire_obj},
            {'adresse': '22 boulevard Anfa, Casablanca', 'nom': 'Studio Anfa', 'ville': 'Casablanca', 'etat': 'Loué', 'metrage': 42.5, 'proprietaire': proprietaire_objs[1]},
            {'adresse': '5 avenue des Nations, Rabat', 'nom': 'Appartement Nations', 'ville': 'Rabat', 'etat': 'Disponible', 'metrage': 98.0, 'proprietaire': proprietaire_objs[2]},
            {'adresse': '10 rue Agdal, Rabat', 'nom': 'Maison Agdal', 'ville': 'Rabat', 'etat': 'En travaux', 'metrage': 120.0, 'proprietaire': proprietaire_objs[3]},
            {'adresse': '47 rue Targa, Marrakech', 'nom': 'Riad Targa', 'ville': 'Marrakech', 'etat': 'Disponible', 'metrage': 150.0, 'proprietaire': proprietaire_obj},
            {'adresse': '3 route de Fès, Meknès', 'nom': 'Appartement Fès', 'ville': 'Meknès', 'etat': 'Loué', 'metrage': 76.0, 'proprietaire': proprietaire_objs[1]},
            {'adresse': '12 rue Ibn Sina, Fès', 'nom': 'Logement Sina', 'ville': 'Fès', 'etat': 'Disponible', 'metrage': 110.0, 'proprietaire': proprietaire_objs[2]},
            {'adresse': '28 rue de Paris, Tanger', 'nom': 'Appartement Paris', 'ville': 'Tanger', 'etat': 'Disponible', 'metrage': 66.0, 'proprietaire': proprietaire_objs[3]},
            {'adresse': '8 place Mohammed V, Casablanca', 'nom': 'Loft Mohammed V', 'ville': 'Casablanca', 'etat': 'Loué', 'metrage': 92.0, 'proprietaire': proprietaire_obj},
            {'adresse': '60 route de Rabat, Salé', 'nom': 'Villa Salé', 'ville': 'Salé', 'etat': 'Disponible', 'metrage': 180.0, 'proprietaire': proprietaire_objs[1]},
        ]

        propriete_objs = []
        for data in propriete_list:
            propriete, _ = Propriete.objects.get_or_create(
                adresse=data['adresse'],
                defaults={
                    'nom': data['nom'],
                    'ville': data['ville'],
                    'etat': data['etat'],
                    'metrage': data['metrage'],
                    'proprietaire': data['proprietaire'],
                },
            )
            propriete_objs.append(propriete)

        for index, prop in enumerate(propriete_objs, start=1):
            selected_agent = agent_objs[index % len(agent_objs)]
            selected_locataire = locataire_objs[index % len(locataire_objs)]
            selected_proprietaire = prop.proprietaire

            Baux.objects.get_or_create(
                id=index + 1,
                defaults={
                    'locataire': selected_locataire,
                    'agent': selected_agent,
                    'propriete': prop,
                    'proprietaire': selected_proprietaire,
                    'prix': 850.00 + index * 50,
                    'date_debut': date(2025, 2, index if index <= 28 else 28),
                    'date_sortie': date(2026, 2, index if index <= 28 else 28),
                },
            )

            Contrat.objects.get_or_create(
                id=index + 1,
                defaults={
                    'agent': selected_agent,
                    'propriete': prop,
                    'pourcentage': 0.03 + (index * 0.005),
                    'prix_min': 800.00 + index * 60,
                    'date_contrat': date(2024, 2, index if index <= 28 else 28),
                    'date_finContrat': date(2026, 2, index if index <= 28 else 28),
                },
            )

            Offre.objects.get_or_create(
                id=index + 1,
                defaults={
                    'agent': selected_agent,
                    'propriete': prop,
                    'prix': 800.00 + index * 55,
                    'pourcentage': 0.02 + (index * 0.003),
                    'date_offre': date(2024, 11, index if index <= 28 else 28),
                },
            )

        for index, prop in enumerate(propriete_objs[:5], start=1):
            Maintenance.objects.get_or_create(
                titre=f'Entretien {index}',
                propriete=prop,
                locataire=locataire_objs[index % len(locataire_objs)],
                date=date(2025, 5, index + 5),
                defaults={'description': f'Entretien périodique et vérification pour {prop.nom}.'},
            )

            demandeLocation.objects.get_or_create(
                propriete=prop,
                locataire=locataire_objs[(index + 1) % len(locataire_objs)],
                dateDemande=date(2024, 12, index + 5),
                defaults={
                    'prix': 900.00 + index * 40,
                    'date_entre': date(2025, 3, index + 5),
                    'date_sortie': date(2026, 3, index + 5),
                },
            )

        print('\nUsers, profils, propriétés et données supplémentaires créés ou existants.')


if __name__ == '__main__':
    try:
        create_profiles()
    except IntegrityError as exc:
        print('Erreur de base de données :', exc)
        sys.exit(1)
