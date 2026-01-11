"""
Recommendations Engine for RSE Sport Monitoring Platform
Generates actionable recommendations based on project data analysis
"""

def generate_recommendations(projects):
    """
    Analyze projects and generate actionable recommendations
    Returns a list of recommendation dictionaries
    """
    
    if not projects:
        return []
    
    recommendations = []
    
    # Analyze budget distribution
    total_budget = sum(p.get('budget', 0) for p in projects)
    avg_budget = total_budget / len(projects) if projects else 0
    
    # Analyze beneficiaries
    total_beneficiaries = sum(p.get('beneficiaries', 0) for p in projects)
    avg_beneficiaries = total_beneficiaries / len(projects) if projects else 0
    
    # Analyze SDG coverage
    all_sdgs = set()
    for p in projects:
        all_sdgs.update(p.get('sdgs', []))
    
    # Analyze sports diversity
    all_sports = set()
    for p in projects:
        all_sports.update(p.get('sports', []))
    
    # Analyze countries
    countries = set(p.get('country', '') for p in projects)
    
    # RECOMMENDATION 1: Budget optimization
    if avg_budget > 0:
        low_budget_projects = [p for p in projects if p.get('budget', 0) < avg_budget * 0.5]
        if len(low_budget_projects) > len(projects) * 0.3:
            recommendations.append({
                "category": "Budget & Ressources",
                "priority": "Haute",
                "title": "Optimiser l'allocation budgétaire",
                "description": f"{len(low_budget_projects)} projets disposent d'un budget inférieur à 50% de la moyenne. Considérer une redistribution des ressources ou recherche de financements complémentaires.",
                "impact": "Amélioration de l'efficacité et de la portée des projets sous-financés",
                "actions": [
                    "Identifier les sources de financement additionnelles (subventions, partenariats)",
                    "Mutualiser les ressources entre projets similaires",
                    "Prioriser les projets à fort impact social"
                ]
            })
    
    # RECOMMENDATION 2: SDG coverage
    if len(all_sdgs) < 5:
        recommendations.append({
            "category": "Alignement ODD",
            "priority": "Moyenne",
            "title": "Diversifier les objectifs de développement durable",
            "description": f"Le portefeuille actuel ne couvre que {len(all_sdgs)} ODD sur 17. Élargir le spectre d'impact pour maximiser la contribution RSE.",
            "impact": "Renforcement de la stratégie RSE globale et meilleure réponse aux enjeux de développement",
            "actions": [
                "Identifier les ODD non couverts mais pertinents pour le secteur sportif",
                "Concevoir des projets pilotes ciblant les ODD manquants",
                "Intégrer de nouveaux partenaires spécialisés"
            ]
        })
    
    # RECOMMENDATION 3: Impact measurement
    projects_with_low_indicators = [
        p for p in projects 
        if p.get('indicator_participants', 0) == 0 or p.get('indicator_sessions', 0) == 0
    ]
    
    if projects_with_low_indicators:
        recommendations.append({
            "category": "Suivi & Évaluation",
            "priority": "Haute",
            "title": "Renforcer le système de mesure d'impact",
            "description": f"{len(projects_with_low_indicators)} projets manquent d'indicateurs quantitatifs robustes. Un suivi rigoureux est essentiel pour démontrer l'impact.",
            "impact": "Meilleure traçabilité, reporting plus crédible, facilitation du fundraising",
            "actions": [
                "Mettre en place des tableaux de bord de suivi mensuel",
                "Former les équipes terrain à la collecte de données",
                "Digitaliser la remontée d'information (applications mobiles)"
            ]
        })
    
    # RECOMMENDATION 4: Geographic expansion
    if len(countries) < 3:
        recommendations.append({
            "category": "Déploiement Géographique",
            "priority": "Moyenne",
            "title": "Étendre la couverture géographique",
            "description": f"Les projets sont concentrés dans {len(countries)} pays. Une expansion régionale renforcerait l'impact continental.",
            "impact": "Portée élargie, partage de bonnes pratiques, économies d'échelle",
            "actions": [
                "Cartographier les opportunités dans les pays voisins",
                "Établir des partenariats avec des fédérations sportives régionales",
                "Adapter les modèles de projets réussis à de nouveaux contextes"
            ]
        })
    
    # RECOMMENDATION 5: Gender equality focus
    women_focused = sum(1 for p in projects if "Femmes" in p.get('target_audience', []))
    if women_focused < len(projects) * 0.3:
        recommendations.append({
            "category": "Égalité des Genres",
            "priority": "Haute",
            "title": "Renforcer l'inclusion des femmes et des filles",
            "description": f"Seulement {women_focused} projets sur {len(projects)} ciblent explicitement les femmes. L'ODD 5 (Égalité des sexes) nécessite une attention accrue.",
            "impact": "Contribution directe à l'ODD 5, transformation sociale, exemple inspirant",
            "actions": [
                "Créer des programmes sportifs dédiés aux filles et femmes",
                "Recruter des entraîneures et modèles féminins",
                "Adapter les infrastructures pour garantir la sécurité et le confort"
            ]
        })
    
    # RECOMMENDATION 6: Disability inclusion
    disability_projects = sum(1 for p in projects if "Personnes en situation de handicap" in p.get('target_audience', []))
    if disability_projects < len(projects) * 0.2:
        recommendations.append({
            "category": "Inclusion & Accessibilité",
            "priority": "Moyenne",
            "title": "Développer le sport adapté et paralympique",
            "description": "Le handisport reste sous-représenté dans le portefeuille. C'est un levier puissant d'inclusion (ODD 10).",
            "impact": "Inclusion des personnes en situation de handicap, visibilité médiatique, innovation sociale",
            "actions": [
                "Nouer des partenariats avec les fédérations handisport",
                "Former les éducateurs sportifs aux techniques adaptées",
                "Rendre les infrastructures accessibles (rampes, vestiaires adaptés)"
            ]
        })
    
    # RECOMMENDATION 7: Environmental sustainability
    high_env_impact = sum(1 for p in projects if p.get('impact_environmental') in ['Fort', 'Très fort'])
    if high_env_impact < len(projects) * 0.3:
        recommendations.append({
            "category": "Environnement & Climat",
            "priority": "Moyenne",
            "title": "Intégrer la dimension environnementale",
            "description": "Peu de projets affichent un impact environnemental fort. Aligner avec les ODD 13, 14, 15 (climat, océans, biodiversité).",
            "impact": "Contribution aux enjeux climatiques, innovation dans le sport durable",
            "actions": [
                "Organiser des événements sportifs éco-responsables (zéro déchet)",
                "Sensibiliser les jeunes athlètes aux enjeux environnementaux",
                "Utiliser des équipements recyclés ou durables"
            ]
        })
    
    # RECOMMENDATION 8: Data-driven decision making
    recommendations.append({
        "category": "Data & Innovation",
        "priority": "Haute",
        "title": "Renforcer la culture data et l'innovation",
        "description": "Capitaliser sur les données collectées pour optimiser les décisions stratégiques et opérationnelles.",
        "impact": "Amélioration continue, anticipation des besoins, meilleure allocation des ressources",
        "actions": [
            "Mettre en place des revues trimestrielles des KPIs",
            "Former les équipes à l'analyse de données",
            "Utiliser des outils de data visualization pour le pilotage",
            "Tester des approches innovantes (IA, coaching digital)"
        ]
    })
    
    return recommendations
