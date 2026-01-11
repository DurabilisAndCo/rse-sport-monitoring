"""
Mock Data Generator for RSE Sport Monitoring Platform
Generates realistic sample projects for demonstration purposes
"""

import random
from datetime import datetime, timedelta

def generate_mock_projects(num_projects=5):
    """Generate realistic mock projects for demonstration"""
    
    mock_projects = []
    
    project_templates = [
        {
            "name": "Programme Jeunesse Sportive Dakar 2024",
            "organization": "Fédération Sénégalaise de Football",
            "country": "Sénégal",
            "location": "Dakar, Parcelles Assainies",
            "sports": ["Football", "Basketball"],
            "description": "Programme d'initiation sportive pour jeunes de quartiers défavorisés, visant à promouvoir l'inclusion sociale et l'éducation par le sport.",
            "budget": 45000,
            "beneficiaries": 500,
            "sport_level": ["Initiation", "Loisir"],
            "target_audience": ["Enfants (0-12 ans)", "Adolescents (13-17 ans)"],
            "sdgs": ["ODD 3: Bonne santé et bien-être", "ODD 4: Éducation de qualité", "ODD 10: Inégalités réduites"],
            "agenda_2063": ["Aspiration 6 : Une Afrique dont le développement est axé sur les populations, qui s'appuie sur le potentiel de ses populations, notamment celles des femmes et des jeunes"],
            "impact_social": "Très fort",
            "impact_environmental": "Moyen",
            "impact_economic": "Moyen"
        },
        {
            "name": "Académie de Basketball Féminin",
            "organization": "Basketball Sans Frontières Afrique",
            "country": "Côte d'Ivoire",
            "location": "Abidjan, Plateau",
            "sports": ["Basketball"],
            "description": "Académie dédiée à la promotion du basketball féminin et au développement des compétences des jeunes filles.",
            "budget": 85000,
            "beneficiaries": 200,
            "sport_level": ["Amateur", "Semi-professionnel"],
            "target_audience": ["Adolescents (13-17 ans)", "Jeunes adultes (18-25 ans)", "Femmes"],
            "sdgs": ["ODD 5: Égalité entre les sexes", "ODD 8: Travail décent et croissance économique", "ODD 3: Bonne santé et bien-être"],
            "agenda_2063": ["Aspiration 6 : Une Afrique dont le développement est axé sur les populations, qui s'appuie sur le potentiel de ses populations, notamment celles des femmes et des jeunes"],
            "impact_social": "Très fort",
            "impact_environmental": "Faible",
            "impact_economic": "Fort"
        },
        {
            "name": "Sport Adapté et Inclusion - Lomé",
            "organization": "Association Togolaise Handisport",
            "country": "Togo",
            "location": "Lomé",
            "sports": ["Basketball fauteuil", "Athlétisme handisport", "Para-natation"],
            "description": "Programme d'accompagnement sportif pour personnes en situation de handicap, favorisant l'autonomie et l'insertion sociale.",
            "budget": 35000,
            "beneficiaries": 150,
            "sport_level": ["Initiation", "Amateur"],
            "target_audience": ["Adolescents (13-17 ans)", "Jeunes adultes (18-25 ans)", "Adultes (26-50 ans)", "Personnes en situation de handicap"],
            "sdgs": ["ODD 10: Inégalités réduites", "ODD 3: Bonne santé et bien-être", "ODD 11: Villes et communautés durables"],
            "agenda_2063": ["Aspiration 1 : Une Afrique prospère basée sur la croissance inclusive et le développement durable"],
            "impact_social": "Très fort",
            "impact_environmental": "Moyen",
            "impact_economic": "Faible"
        },
        {
            "name": "E-Sport Academy West Africa",
            "organization": "Digital Sports Africa",
            "country": "Ghana",
            "location": "Accra",
            "sports": ["FIFA", "League of Legends", "Mobile Legends"],
            "description": "Première académie e-sport en Afrique de l'Ouest, formant les jeunes talents aux métiers du gaming professionnel et du streaming.",
            "budget": 120000,
            "beneficiaries": 300,
            "sport_level": ["Amateur", "Semi-professionnel", "Professionnel"],
            "target_audience": ["Adolescents (13-17 ans)", "Jeunes adultes (18-25 ans)"],
            "sdgs": ["ODD 4: Éducation de qualité", "ODD 8: Travail décent et croissance économique", "ODD 9: Industrie, innovation et infrastructure"],
            "agenda_2063": ["Aspiration 1 : Une Afrique prospère basée sur la croissance inclusive et le développement durable"],
            "impact_social": "Fort",
            "impact_environmental": "Faible",
            "impact_economic": "Très fort"
        },
        {
            "name": "Rugby pour la Paix - Grands Lacs",
            "organization": "Peace Through Sport International",
            "country": "RD Congo",
            "location": "Goma, Nord-Kivu",
            "sports": ["Rugby", "Rugby à 7"],
            "description": "Utilisation du rugby comme outil de réconciliation et cohésion sociale dans les zones post-conflit.",
            "budget": 65000,
            "beneficiaries": 800,
            "sport_level": ["Initiation", "Loisir"],
            "target_audience": ["Enfants (0-12 ans)", "Adolescents (13-17 ans)", "Jeunes adultes (18-25 ans)"],
            "sdgs": ["ODD 16: Paix, justice et institutions efficaces", "ODD 3: Bonne santé et bien-être", "ODD 10: Inégalités réduites"],
            "agenda_2063": ["Aspiration 4 : Une Afrique vivant dans la paix et la sécurité"],
            "impact_social": "Très fort",
            "impact_environmental": "Moyen",
            "impact_economic": "Moyen"
        },
        {
            "name": "Natation Scolaire - Coastal Initiative",
            "organization": "Swimming Federation Benin",
            "country": "Bénin",
            "location": "Cotonou",
            "sports": ["Natation"],
            "description": "Programme de natation dans les écoles primaires pour réduire les noyades et promouvoir la sécurité aquatique.",
            "budget": 28000,
            "beneficiaries": 1200,
            "sport_level": ["Initiation"],
            "target_audience": ["Enfants (0-12 ans)"],
            "sdgs": ["ODD 3: Bonne santé et bien-être", "ODD 4: Éducation de qualité", "ODD 6: Eau propre et assainissement"],
            "agenda_2063": ["Aspiration 1 : Une Afrique prospère basée sur la croissance inclusive et le développement durable"],
            "impact_social": "Fort",
            "impact_environmental": "Moyen",
            "impact_economic": "Faible"
        }
    ]
    
    # Select random projects from templates
    selected = random.sample(project_templates, min(num_projects, len(project_templates)))
    
    for i, template in enumerate(selected):
        # Generate dates
        start_date = datetime.now() - timedelta(days=random.randint(30, 365))
        end_date = start_date + timedelta(days=random.randint(180, 730))
        
        project = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": template["name"],
            "organization": template["organization"],
            "country": template["country"],
            "location": template["location"],
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "description": template["description"],
            "budget": template["budget"],
            "beneficiaries": template["beneficiaries"],
            "sports": template["sports"],
            "sport_level": template["sport_level"],
            "target_audience": template["target_audience"],
            "infrastructure": f"Infrastructures municipales, {random.choice(['Stade', 'Gymnase', 'Terrain synthétique', 'Centre sportif'])}",
            "sdgs": template["sdgs"],
            "agenda_2063": template["agenda_2063"],
            "alignment_description": f"Ce projet s'aligne avec les objectifs de développement durable en promouvant {random.choice(['l\\'inclusion sociale', 'la santé publique', 'l\\'égalité des genres', 'l\\'éducation'])} à travers le sport.",
            "indicator_participants": random.randint(50, 500),
            "indicator_sessions": random.randint(20, 200),
            "indicator_hours": random.randint(100, 2000),
            "impact_social": template["impact_social"],
            "impact_environmental": template["impact_environmental"],
            "impact_economic": template["impact_economic"],
            "monitoring_tools": random.sample(["Questionnaires", "Entretiens", "Observations terrain", "Données analytiques", "Reporting mensuel"], 3),
            "monitoring_frequency": random.choice(["Mensuel", "Trimestriel", "Semestriel"]),
            "additional_notes": f"Projet pilote avec potentiel d'expansion régionale. Partenariats établis avec {random.randint(2, 8)} organisations locales."
        }
        
        mock_projects.append(project)
    
    return mock_projects
