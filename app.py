import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
from io import BytesIO

# Import custom modules
try:
    from mock_data import generate_mock_projects
    from recommendations import generate_recommendations
except:
    # Fallback if modules don't exist
    def generate_mock_projects(n=5):
        return []
    def generate_recommendations(projects):
        return []

# Configuration de la page
st.set_page_config(
    page_title="Data Monitoring – Projet RSE & Sport | Durabilis & Co",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# DATA STRUCTURES - Sports, SDGs, Agenda 2063
# ============================================================================

# Comprehensive Sports List (categorized)
SPORTS_LIST = {
    "Sports Collectifs": [
        "Football", "Basketball", "Volleyball", "Handball", "Rugby", "Hockey sur gazon",
        "Hockey sur glace", "Water-polo", "Baseball", "Softball", "Cricket", "Futsal",
        "Beach-volley", "Rugby à 7", "Football américain", "Polo", "Lacrosse", "Kabaddi",
        "Sepak takraw", "Ultimate frisbee", "Dodgeball", "Netball", "Hurling", "Camogie"
    ],
    "Sports Individuels": [
        "Athlétisme", "Natation", "Cyclisme", "Tennis", "Badminton", "Tennis de table",
        "Golf", "Boxe", "Judo", "Karaté", "Taekwondo", "Lutte", "Escrime", "Tir",
        "Tir à l'arc", "Équitation", "Gymnastique", "Haltérophilie", "Triathlon",
        "Pentathlon moderne", "Ski alpin", "Ski de fond", "Snowboard", "Patinage artistique",
        "Patinage de vitesse", "Biathlon", "Saut à ski", "Combiné nordique", "Skeleton",
        "Bobsleigh", "Luge", "Curling", "Surf", "Skateboard", "Escalade sportive",
        "Voile", "Aviron", "Canoë-kayak", "Plongeon", "Nage synchronisée", "Para-natation"
    ],
    "Sports Paralympiques": [
        "Athlétisme handisport", "Natation handisport", "Basketball fauteuil", "Rugby fauteuil",
        "Tennis fauteuil", "Tennis de table handisport", "Escrime fauteuil", "Boccia",
        "Goalball", "Cécifoot", "Volley assis", "Para-cyclisme", "Para-équitation",
        "Para-aviron", "Para-canoë", "Para-judo", "Para-tir", "Para-tir à l'arc",
        "Para-triathlon", "Para-haltérophilie", "Para-taekwondo", "Para-badminton"
    ],
    "Sports Traditionnels": [
        "Lutte sénégalaise", "Capoeira", "Kung-fu", "Wushu", "Sumo", "Muay Thai",
        "Kendo", "Aïkido", "Vovinam", "Silat", "Pétanque", "Boules lyonnaises",
        "Boomerang", "Sports gaéliques", "Pelote basque"
    ],
    "E-Sport": [
        "League of Legends", "Dota 2", "Counter-Strike", "Valorant", "Fortnite",
        "FIFA", "eFootball", "NBA 2K", "Rocket League", "Overwatch", "StarCraft",
        "Rainbow Six Siege", "Call of Duty", "PUBG", "Mobile Legends"
    ],
    "Sports de Combat": [
        "MMA", "Kickboxing", "Boxe française (savate)", "Sambo", "Krav Maga",
        "Jiu-jitsu brésilien", "Catch", "Pancrace"
    ],
    "Sports Nautiques": [
        "Planche à voile", "Kitesurf", "Stand-up paddle", "Wakeboard", "Ski nautique",
        "Jet-ski", "Plongée sous-marine", "Nage en eau libre", "Sauvetage côtier"
    ],
    "Sports Aériens": [
        "Parachutisme", "Parapente", "Vol à voile", "Deltaplane", "Base jump", "Wingsuit"
    ],
    "Sports Mécaniques": [
        "Formule 1", "Rallye", "MotoGP", "Karting", "Endurance moto", "Trial",
        "Speedway", "Rallycross", "Drift", "Formule E"
    ],
    "Sports de Montagne": [
        "Alpinisme", "Randonnée", "Trail running", "VTT", "Ski-alpinisme",
        "Cascade de glace", "Via ferrata", "Slackline"
    ],
    "Autres Sports": [
        "Danse sportive", "Cheerleading", "Crossfit", "Fitness", "Yoga sportif",
        "Parkour", "Roller", "BMX", "Squash", "Padel", "Billard", "Fléchettes",
        "Bowling", "Arts martiaux mixtes", "Powerlifting", "Strongman"
    ]
}

# Flatten sports list
ALL_SPORTS = []
for category, sports in SPORTS_LIST.items():
    ALL_SPORTS.extend(sports)
ALL_SPORTS = sorted(set(ALL_SPORTS))

# 17 SDGs
SDGS = [
    {"num": 1, "title": "Pas de pauvreté", "color": "#E5243B"},
    {"num": 2, "title": "Faim « zéro »", "color": "#DDA63A"},
    {"num": 3, "title": "Bonne santé et bien-être", "color": "#4C9F38"},
    {"num": 4, "title": "Éducation de qualité", "color": "#C5192D"},
    {"num": 5, "title": "Égalité entre les sexes", "color": "#FF3A21"},
    {"num": 6, "title": "Eau propre et assainissement", "color": "#26BDE2"},
    {"num": 7, "title": "Énergie propre et d'un coût abordable", "color": "#FCC30B"},
    {"num": 8, "title": "Travail décent et croissance économique", "color": "#A21942"},
    {"num": 9, "title": "Industrie, innovation et infrastructure", "color": "#FD6925"},
    {"num": 10, "title": "Inégalités réduites", "color": "#DD1367"},
    {"num": 11, "title": "Villes et communautés durables", "color": "#FD9D24"},
    {"num": 12, "title": "Consommation et production responsables", "color": "#BF8B2E"},
    {"num": 13, "title": "Mesures relatives à la lutte contre les changements climatiques", "color": "#3F7E44"},
    {"num": 14, "title": "Vie aquatique", "color": "#0A97D9"},
    {"num": 15, "title": "Vie terrestre", "color": "#56C02B"},
    {"num": 16, "title": "Paix, justice et institutions efficaces", "color": "#00689D"},
    {"num": 17, "title": "Partenariats pour la réalisation des objectifs", "color": "#19486A"},
]

SDG_OPTIONS = [f"ODD {sdg['num']}: {sdg['title']}" for sdg in SDGS]

# Agenda 2063
AGENDA_2063 = [
    "Aspiration 1 : Une Afrique prospère basée sur la croissance inclusive et le développement durable",
    "Aspiration 2 : Un continent intégré, politiquement uni, ancré dans les idéaux du panafricanisme",
    "Aspiration 3 : Une Afrique où règnent la bonne gouvernance, la démocratie, le respect des droits humains, la justice et l'État de droit",
    "Aspiration 4 : Une Afrique vivant dans la paix et la sécurité",
    "Aspiration 5 : Une Afrique dotée d'une identité culturelle, d'un patrimoine, de valeurs et d'une éthique forts",
    "Aspiration 6 : Une Afrique dont le développement est axé sur les populations, qui s'appuie sur le potentiel de ses populations, notamment celles des femmes et des jeunes",
    "Aspiration 7 : Une Afrique forte, résiliente et influente, acteur et partenaire mondial"
]

# ============================================================================
# DURABILIS & CO BRANDING - FIXED SIDEBAR CONTRAST
# ============================================================================

DURABILIS_COLORS = {
    "primary_blue": "#00A9E0",
    "secondary_blue": "#2E3192",
    "dark_grey": "#58595B",
    "light_grey": "#BCBEC0",
    "white": "#FFFFFF",
    "accent": "#00A9E0"
}

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    .main {{
        padding: 1.5rem 2rem;
        background-color: #f8f9fa;
    }}
    
    h1, h2, h3 {{
        color: {DURABILIS_COLORS['secondary_blue']};
        font-weight: 700;
    }}
    
    /* CRITICAL FIX: Sidebar contrast */
    [data-testid="stSidebar"] {{
        background-color: {DURABILIS_COLORS['secondary_blue']};
    }}
    
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] .stRadio > label {{
        color: white !important;
        font-weight: 600;
    }}
    
    [data-testid="stSidebar"] .stRadio > div {{
        background-color: rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        border-radius: 6px;
    }}
    
    [data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] {{
        background-color: rgba(255, 255, 255, 0.15);
        padding: 0.75rem;
        border-radius: 6px;
        margin: 0.25rem 0;
        transition: all 0.3s ease;
    }}
    
    [data-testid="stSidebar"] .stRadio label[data-baseweb="radio"]:hover {{
        background-color: {DURABILIS_COLORS['primary_blue']};
        transform: translateX(4px);
    }}
    
    [data-testid="stSidebar"] .stRadio input:checked + div {{
        background-color: {DURABILIS_COLORS['primary_blue']} !important;
    }}
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] hr {{
        border-color: rgba(255, 255, 255, 0.3);
    }}
    
    /* Title banner */
    .platform-title {{
        background: linear-gradient(135deg, {DURABILIS_COLORS['secondary_blue']} 0%, {DURABILIS_COLORS['primary_blue']} 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    
    .platform-title h1 {{
        color: white !important;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }}
    
    .platform-subtitle {{
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {DURABILIS_COLORS['primary_blue']};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background-color: {DURABILIS_COLORS['secondary_blue']};
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: white;
        border-radius: 6px 6px 0 0;
        color: {DURABILIS_COLORS['dark_grey']};
        font-weight: 600;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {DURABILIS_COLORS['primary_blue']};
        color: white;
    }}
    
    /* Metrics */
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
        border-left: 4px solid {DURABILIS_COLORS['primary_blue']};
    }}
    
    @media (max-width: 768px) {{
        .main {{
            padding: 1rem;
        }}
        .platform-title h1 {{
            font-size: 1.8rem;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'projects' not in st.session_state:
    st.session_state.projects = []

if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = False

# ============================================================================
# MAIN APPLICATION
# ============================================================================

# Platform Title Banner
st.markdown(f"""
    <div class="platform-title">
        <h1>📊 Data Monitoring – Projet RSE & Sport</h1>
        <p class="platform-subtitle">Plateforme de suivi et d'analyse des projets RSE dans le secteur sportif | Durabilis & Co</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - FIXED CONTRAST
# ============================================================================

# Logo - Add your logo URL here for deployment
# st.sidebar.image("path_to_your_logo.png", use_container_width=True)
try:
    # Uncomment and update with your hosted logo URL
    # st.sidebar.image("https://your-domain.com/logo.png", use_container_width=True)
    pass
except:
    pass

st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("---")

# Demo Mode Toggle
demo_mode = st.sidebar.checkbox(
    "🎬 Mode Démonstration",
    value=st.session_state.demo_mode,
    help="Charger des données fictives pour prévisualiser la plateforme"
)

if demo_mode != st.session_state.demo_mode:
    st.session_state.demo_mode = demo_mode
    if demo_mode and not st.session_state.projects:
        st.session_state.projects = generate_mock_projects(6)
        st.rerun()

st.sidebar.markdown("---")

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["📋 Créer un Projet", "📊 Tableau de Bord", "💡 Recommandations", "📄 Rapport Professionnel", "🗂️ Gérer les Projets"],
    index=0 if not st.session_state.projects else 1
)

# ============================================================================
# PAGE 1: CREATE PROJECT
# ============================================================================

if page == "📋 Créer un Projet":
    
    tabs = st.tabs([
        "1️⃣ Informations Générales",
        "2️⃣ Sport & Discipline",
        "3️⃣ Alignement ODD / Agenda 2063",
        "4️⃣ Indicateurs & Suivi"
    ])
    
    with tabs[0]:
        st.subheader("📝 Informations Générales du Projet")
        
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input("Nom du Projet *", placeholder="Ex: Programme Jeunesse Sportive 2024")
            project_country = st.selectbox(
                "Pays *",
                ["Sénégal", "Côte d'Ivoire", "Bénin", "Burkina Faso", "Mali", "Niger", "Togo", 
                 "Ghana", "Nigeria", "Kenya", "Afrique du Sud", "Cameroun", "RD Congo", "France", "Autre"]
            )
            project_start_date = st.date_input("Date de début *")
        
        with col2:
            project_organization = st.text_input("Organisation/Porteur du projet *")
            project_location = st.text_input("Localisation *")
            project_end_date = st.date_input("Date de fin prévue")
        
        project_description = st.text_area("Description du projet *", height=120)
        project_budget = st.number_input("Budget (en €)", min_value=0, step=1000, value=0)
        project_beneficiaries = st.number_input("Nombre de bénéficiaires estimés", min_value=0, step=10, value=0)
    
    with tabs[1]:
        st.subheader("⚽ Sport & Discipline")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sport_category = st.selectbox("Catégorie de sport *", [""] + list(SPORTS_LIST.keys()))
            
            if sport_category:
                selected_sports = st.multiselect("Sélectionner le(s) sport(s) *", SPORTS_LIST[sport_category])
            else:
                selected_sports = st.multiselect("Ou rechercher dans tous les sports", ALL_SPORTS)
        
        with col2:
            sport_level = st.multiselect(
                "Niveau de pratique *",
                ["Initiation", "Loisir", "Amateur", "Semi-professionnel", "Professionnel", "Élite/Haut niveau"]
            )
            
            target_audience = st.multiselect(
                "Public cible *",
                ["Enfants (0-12 ans)", "Adolescents (13-17 ans)", "Jeunes adultes (18-25 ans)", 
                 "Adultes (26-50 ans)", "Seniors (50+ ans)", "Personnes en situation de handicap",
                 "Femmes", "Hommes", "Mixte"]
            )
        
        sport_infrastructure = st.text_area("Infrastructures utilisées", height=80)
    
    with tabs[2]:
        st.subheader("🌍 Alignement ODD (Agenda 2030) & Agenda 2063")
        
        st.markdown("##### 🎯 Objectifs de Développement Durable (ODD)")
        
        sdg_cols = st.columns(3)
        selected_sdgs = []
        
        for idx, sdg in enumerate(SDGS):
            with sdg_cols[idx % 3]:
                sdg_label = f"ODD {sdg['num']}: {sdg['title'][:30]}..."
                if st.checkbox(sdg_label, key=f"sdg_{sdg['num']}"):
                    selected_sdgs.append(f"ODD {sdg['num']}: {sdg['title']}")
        
        st.markdown("---")
        
        st.markdown("##### 🌍 Agenda 2063 de l'Union Africaine")
        selected_agenda_2063 = st.multiselect("Aspirations de l'Agenda 2063", AGENDA_2063)
        
        alignment_description = st.text_area("Description de l'alignement stratégique", height=100)
    
    with tabs[3]:
        st.subheader("📈 Indicateurs & Suivi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Indicateurs quantitatifs**")
            indicator_participants = st.number_input("Nombre de participants", min_value=0, step=1)
            indicator_sessions = st.number_input("Nombre de sessions/événements", min_value=0, step=1)
            indicator_hours = st.number_input("Heures d'activité totales", min_value=0, step=1)
            
        with col2:
            st.markdown("**Indicateurs qualitatifs**")
            impact_social = st.select_slider("Impact social", options=["Très faible", "Faible", "Moyen", "Fort", "Très fort"], value="Moyen")
            impact_environmental = st.select_slider("Impact environnemental", options=["Très faible", "Faible", "Moyen", "Fort", "Très fort"], value="Moyen")
            impact_economic = st.select_slider("Impact économique", options=["Très faible", "Faible", "Moyen", "Fort", "Très fort"], value="Moyen")
        
        monitoring_tools = st.multiselect(
            "Outils de suivi utilisés",
            ["Questionnaires", "Entretiens", "Observations terrain", "Données analytiques",
             "Reporting mensuel", "Évaluation externe", "Auto-évaluation", "Tableaux de bord"]
        )
        
        monitoring_frequency = st.selectbox("Fréquence de suivi", ["Hebdomadaire", "Bimensuel", "Mensuel", "Trimestriel", "Semestriel", "Annuel"])
        
        additional_notes = st.text_area("Notes et commentaires additionnels", height=100)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        submit_button = st.button("💾 Enregistrer le Projet", use_container_width=True, type="primary")
    
    if submit_button:
        if not project_name or not project_organization:
            st.error("❌ Veuillez remplir au minimum le nom du projet et l'organisation.")
        elif not selected_sports:
            st.error("❌ Veuillez sélectionner au moins un sport.")
        else:
            project_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": project_name,
                "organization": project_organization,
                "country": project_country,
                "location": project_location,
                "start_date": str(project_start_date),
                "end_date": str(project_end_date),
                "description": project_description,
                "budget": project_budget,
                "beneficiaries": project_beneficiaries,
                "sports": selected_sports,
                "sport_level": sport_level,
                "target_audience": target_audience,
                "infrastructure": sport_infrastructure,
                "sdgs": selected_sdgs,
                "agenda_2063": selected_agenda_2063,
                "alignment_description": alignment_description,
                "indicator_participants": indicator_participants,
                "indicator_sessions": indicator_sessions,
                "indicator_hours": indicator_hours,
                "impact_social": impact_social,
                "impact_environmental": impact_environmental,
                "impact_economic": impact_economic,
                "monitoring_tools": monitoring_tools,
                "monitoring_frequency": monitoring_frequency,
                "additional_notes": additional_notes
            }
            
            st.session_state.projects.append(project_data)
            st.success(f"✅ Projet '{project_name}' enregistré avec succès!")
            st.balloons()

# ============================================================================
# PAGE 2: DASHBOARD
# ============================================================================

elif page == "📊 Tableau de Bord":
    
    if not st.session_state.projects:
        st.warning("Aucun projet enregistré. Activez le Mode Démonstration ou créez un projet.")
    else:
        st.header("📊 Tableau de Bord RSE & Sport")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_projects = len(st.session_state.projects)
        total_budget = sum(p.get('budget', 0) for p in st.session_state.projects)
        total_beneficiaries = sum(p.get('beneficiaries', 0) for p in st.session_state.projects)
        unique_countries = len(set(p.get('country', '') for p in st.session_state.projects))
        
        with col1:
            st.metric("Projets Totaux", total_projects, delta=None)
        
        with col2:
            st.metric("Budget Total", f"{total_budget:,.0f} €", delta=None)
        
        with col3:
            st.metric("Bénéficiaires", f"{total_beneficiaries:,}", delta=None)
        
        with col4:
            st.metric("Pays Couverts", unique_countries, delta=None)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌍 Distribution Géographique")
            country_counts= {}
            for p in st.session_state.projects:
                country = p.get('country', 'Inconnu')
                country_counts[country] = country_counts.get(country, 0) + 1
            
            fig_geo = px.bar(
                x=list(country_counts.keys()),
                y=list(country_counts.values()),
                labels={'x': 'Pays', 'y': 'Nombre de projets'},
                color=list(country_counts.values()),
                color_continuous_scale='Blues'
            )
            fig_geo.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig_geo, use_container_width=True)
        
        with col2:
            st.subheader("⚽ Sports Pratiqués")
            sport_counts = {}
            for p in st.session_state.projects:
                for sport in p.get('sports', []):
                    sport_counts[sport] = sport_counts.get(sport, 0) + 1
            
            fig_sports = px.pie(
                names=list(sport_counts.keys()),
                values=list(sport_counts.values()),
                hole=0.4
            )
            fig_sports.update_layout(height=300)
            st.plotly_chart(fig_sports, use_container_width=True)
        
        st.markdown("---")
        
        # SDG Alignment
        st.subheader("🎯 Alignement ODD")
        
        sdg_counts = {}
        for p in st.session_state.projects:
            for sdg_text in p.get('sdgs', []):
                sdg_num = int(sdg_text.split(':')[0].replace('ODD', '').strip())
                sdg_counts[sdg_num] = sdg_counts.get(sdg_num, 0) + 1
        
        sdg_data = []
        for sdg in SDGS:
            count = sdg_counts.get(sdg['num'], 0)
            sdg_data.append({
                'ODD': f"ODD {sdg['num']}",
                'Projets': count,
                'Couleur': sdg['color']
            })
        
        df_sdg = pd.DataFrame(sdg_data)
        
        fig_sdg = px.bar(
            df_sdg,
            x='ODD',
            y='Projets',
            color='Projets',
            color_continuous_scale='Viridis'
        )
        fig_sdg.update_layout(height=400)
        st.plotly_chart(fig_sdg, use_container_width=True)
        
        st.markdown("---")
        
        # Impact Analysis
        st.subheader("📈 Analyse d'Impact")
        
        impact_map = {"Très faible": 1, "Faible": 2, "Moyen": 3, "Fort": 4, "Très fort": 5}
        
        impact_data = {
            'Dimension': ['Social', 'Environnemental', 'Économique'],
            'Score Moyen': [
                sum(impact_map.get(p.get('impact_social', 'Moyen'), 3) for p in st.session_state.projects) / len(st.session_state.projects),
                sum(impact_map.get(p.get('impact_environmental', 'Moyen'), 3) for p in st.session_state.projects) / len(st.session_state.projects),
                sum(impact_map.get(p.get('impact_economic', 'Moyen'), 3) for p in st.session_state.projects) / len(st.session_state.projects)
            ]
        }
        
        fig_impact = go.Figure(data=go.Scatterpolar(
            r=impact_data['Score Moyen'],
            theta=impact_data['Dimension'],
            fill='toself',
            fillcolor='rgba(0, 169, 224, 0.3)',
            line=dict(color='rgb(0, 169, 224)')
        ))
        fig_impact.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            height=400
        )
        st.plotly_chart(fig_impact, use_container_width=True)

# ============================================================================
# PAGE 3: RECOMMENDATIONS
# ============================================================================

elif page == "💡 Recommandations":
    
    st.header("💡 Recommandations Stratégiques")
    
    if not st.session_state.projects:
        st.warning("Aucun projet enregistré. Activez le Mode Démonstration ou créez un projet.")
    else:
        st.info("Recommandations générées automatiquement basées sur l'analyse de vos projets RSE.")
        
        recommendations = generate_recommendations(st.session_state.projects)
        
        if recommendations:
            for idx, rec in enumerate(recommendations):
                priority_color = {"Haute": "🔴", "Moyenne": "🟡", "Basse": "🟢"}
                
                with st.expander(f"{priority_color.get(rec['priority'], '🔵')} {rec['title']}", expanded=idx < 2):
                    st.markdown(f"**Catégorie:** {rec['category']}")
                    st.markdown(f"**Priorité:** {rec['priority']}")
                    st.markdown(f"**Description:** {rec['description']}")
                    st.markdown(f"**Impact attendu:** {rec['impact']}")
                    
                    st.markdown("**Actions recommandées:**")
                    for action in rec['actions']:
                        st.markdown(f"- {action}")
        else:
            st.info("Aucune recommandation générée pour le moment.")

# ============================================================================
# PAGE 4: PROFESSIONAL REPORT
# ============================================================================

elif page == "📄 Rapport Professionnel":
    
    st.header("📄 Rapport Professionnel RSE & Sport")
    
    if not st.session_state.projects:
        st.warning("Aucun projet enregistré. Activez le Mode Démonstration ou créez un projet.")
    else:
        st.info("Générez un rapport professionnel prêt à être partagé avec vos parties prenantes.")
        
        # Report Configuration
        with st.form("report_config"):
            st.subheader("Configuration du Rapport")
            
            report_title = st.text_input("Titre du rapport", value="Rapport RSE - Projets Sport & Développement Durable")
            report_company = st.text_input("Nom de l'organisation", value="Durabilis & Co")
            report_year = st.number_input("Année", min_value=2020, max_value=2030, value=datetime.now().year)
            
            include_summary = st.checkbox("Inclure le résumé exécutif", value=True)
            include_dashboards = st.checkbox("Inclure les visualisations", value=True)
            include_recommendations = st.checkbox("Inclure les recommandations", value=True)
            
            generate_report = st.form_submit_button("📥 Générer le Rapport (HTML)", type="primary")
        
        if generate_report:
            # Generate HTML Report
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{report_title}</title>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
                    
                    body {{
                        font-family: 'Inter', sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 1200px;
                        margin: 0 auto;
                        padding: 40px;
                    }}
                    
                    .cover-page {{
                        text-align: center;
                        padding: 100px 0;
                        background: linear-gradient(135deg, #2E3192 0%, #00A9E0 100%);
                        color: white;
                        margin: -40px -40px 40px -40px;
                    }}
                    
                    .cover-page h1 {{
                        font-size: 3rem;
                        margin: 20px 0;
                    }}
                    
                    .cover-page .year {{
                        font-size: 2rem;
                        font-weight: 300;
                    }}
                    
                    h2 {{
                        color: #2E3192;
                        border-bottom: 3px solid #00A9E0;
                        padding-bottom: 10px;
                    }}
                    
                    .metric-grid {{
                        display: grid;
                        grid-template-columns: repeat(4, 1fr);
                        gap: 20px;
                        margin: 30px 0;
                    }}
                    
                    .metric-card {{
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border-left: 4px solid #00A9E0;
                    }}
                    
                    .metric-value {{
                        font-size: 2rem;
                        font-weight: 700;
                        color: #2E3192;
                    }}
                    
                    .metric-label {{
                        color: #666;
                        font-size: 0.9rem;
                    }}
                    
                    .project-list {{
                        margin: 20px 0;
                    }}
                    
                    .project-item {{
                        background: #f8f9fa;
                        padding: 15px;
                        margin: 10px 0;
                        border-radius: 6px;
                        border-left: 4px solid #00A9E0;
                    }}
                    
                    .recommendation {{
                        background: #fff9e6;
                        padding: 15px;
                        margin: 15px 0;
                        border-radius: 6px;
                        border-left: 4px solid #FCC30B;
                    }}
                    
                    .footer {{
                        text-align: center;
                        margin-top: 60px;
                        padding-top: 20px;
                        border-top: 2px solid #eee;
                        color: #666;
                    }}
                </style>
            </head>
            <body>
                <div class="cover-page">
                    <h1>{report_title}</h1>
                    <p class="year">{report_year}</p>
                    <p>{report_company}</p>
                </div>
                
                <h2>📋 Sommaire</h2>
                <ul>
                    <li>Résumé Exécutif</li>
                    <li>Vue d'Ensemble des Projets</li>
                    <li>Analyse des Indicateurs</li>
                    <li>Recommandations Stratégiques</li>
                    <li>Conclusion</li>
                </ul>
                
                {f'''
                <h2>📊 Résumé Exécutif</h2>
                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="metric-value">{len(st.session_state.projects)}</div>
                        <div class="metric-label">Projets</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{sum(p.get('budget', 0) for p in st.session_state.projects):,.0f} €</div>
                        <div class="metric-label">Budget Total</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{sum(p.get('beneficiaries', 0) for p in st.session_state.projects):,}</div>
                        <div class="metric-label">Bénéficiaires</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{len(set(p.get('country', '') for p in st.session_state.projects))}</div>
                        <div class="metric-label">Pays</div>
                    </div>
                </div>
                ''' if include_summary else ''}
                
                <h2>🗂️ Liste des Projets</h2>
                <div class="project-list">
                    {''.join([f'''
                    <div class="project-item">
                        <h3>{p.get('name', 'Sans nom')}</h3>
                        <p><strong>Organisation:</strong> {p.get('organization', 'N/A')}</p>
                        <p><strong>Pays:</strong> {p.get('country', 'N/A')}</p>
                        <p><strong>Sports:</strong> {', '.join(p.get('sports', []))}</p>
                        <p><strong>Bénéficiaires:</strong> {p.get('beneficiaries', 0)}</p>
                        <p><strong>Budget:</strong> {p.get('budget', 0):,.0f} €</p>
                    </div>
                    ''' for p in st.session_state.projects])}
                </div>
                
                {f'''
                <h2>💡 Recommandations Stratégiques</h2>
                {''.join([f'''
                <div class="recommendation">
                    <h3>{rec.get('title', '')}</h3>
                    <p><strong>Catégorie:</strong> {rec.get('category', '')}</p>
                    <p><strong>Priorité:</strong> {rec.get('priority', '')}</p>
                    <p>{rec.get('description', '')}</p>
                    <p><strong>Impact:</strong> {rec.get('impact', '')}</p>
                    <ul>
                        {''.join([f'<li>{action}</li>' for action in rec.get('actions', [])])}
                    </ul>
                </div>
                ''' for rec in generate_recommendations(st.session_state.projects)])}
                ''' if include_recommendations else ''}
                
                <h2>🎯 Conclusion</h2>
                <p>
                    Ce rapport présente une vue d'ensemble des projets RSE dans le secteur sportif menés par {report_company}.
                    Les données démontrent un engagement fort en faveur du développement durable et de l'inclusion sociale à travers le sport.
                </p>
                <p>
                    Les recommandations formulées visent à renforcer l'impact de ces initiatives et à maximiser leur contribution aux Objectifs de Développement Durable.
                </p>
                
                <div class="footer">
                    <p>Rapport généré le {datetime.now().strftime('%d/%m/%Y')}</p>
                    <p>{report_company} - Data & Impact</p>
                </div>
            </body>
            </html>
            """
            
            # Download button
            st.download_button(
                label="📥 Télécharger le Rapport HTML",
                data=html_content,
                file_name=f"rapport_rse_sport_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html"
            )
            
            st.success("✅ Rapport généré avec succès!")
            
            # Preview
            with st.expander("👁️ Prévisualiser le rapport"):
                st.components.v1.html(html_content, height=800, scrolling=True)

# ============================================================================
# PAGE 5: MANAGE PROJECTS
# ============================================================================

elif page == "🗂️ Gérer les Projets":
    
    st.header("🗂️ Gestion des Projets")
    
    if not st.session_state.projects:
        st.warning("Aucun projet enregistré.")
    else:
        st.success(f"**{len(st.session_state.projects)} projet(s) enregistré(s)**")
        
        for idx, project in enumerate(st.session_state.projects):
            with st.expander(f"📁 {project.get('name', 'Projet sans nom')} - {project.get('organization', 'N/A')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Pays:** {project.get('country', 'N/A')}")
                    st.write(f"**Localisation:** {project.get('location', 'N/A')}")
                    st.write(f"**Budget:** {project.get('budget', 0):,} €")
                    st.write(f"**Bénéficiaires:** {project.get('beneficiaries', 0)}")
                
                with col2:
                    st.write(f"**Sport(s):** {', '.join(project.get('sports', []))}")
                    st.write(f"**ODD:** {len(project.get('sdgs', []))}")
                    st.write(f"**Agenda 2063:** {len(project.get('agenda_2063', []))}")
                
                if project.get('description'):
                    st.markdown("**Description:**")
                    st.write(project['description'])
                
                if st.button(f"🗑️ Supprimer", key=f"del_{idx}"):
                    st.session_state.projects.pop(idx)
                    st.rerun()
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Exporter tous les projets (CSV)"):
                df_export = pd.DataFrame(st.session_state.projects)
                csv = df_export.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Télécharger CSV",
                    data=csv,
                    file_name=f'projets_rse_sport_{datetime.now().strftime("%Y%m%d")}.csv',
                    mime='text/csv',
                )
        
        with col2:
            if st.button("🗑️ Effacer tous les projets"):
                st.session_state.projects = []
                st.rerun()

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #58595B; padding: 1rem;'>
    <p><strong>Durabilis & Co</strong> - Data & Impact</p>
    <p style='font-size: 0.9rem;'>💻 Plateforme optimisée pour Desktop, Tablette et Mobile</p>
</div>
""", unsafe_allow_html=True)
