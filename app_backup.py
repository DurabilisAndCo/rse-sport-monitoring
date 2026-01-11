import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

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
        "Voile", "Aviron", "Canoë-kayak", "Plongeon", "Nage synchronisée"
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

# Flatten sports list for simple dropdown
ALL_SPORTS = []
for category, sports in SPORTS_LIST.items():
    ALL_SPORTS.extend(sports)
ALL_SPORTS = sorted(set(ALL_SPORTS))

# 17 Sustainable Development Goals (SDGs / ODD)
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

# Agenda 2063 Aspirations (African Union)
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
# CUSTOM STYLING - Durabilis & Co Branding
# ============================================================================

# Color palette extracted from Durabilis & Co logo
DURABILIS_COLORS = {
    "primary_blue": "#00A9E0",      # Bright cyan-blue
    "secondary_blue": "#2E3192",     # Deep navy blue
    "dark_grey": "#58595B",          # Professional dark grey
    "light_grey": "#BCBEC0",         # Light grey for backgrounds
    "white": "#FFFFFF",
    "accent": "#00A9E0"              # For highlights
}

st.markdown(f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Main container */
    .main {{
        padding: 1.5rem 2rem;
        background-color: #f8f9fa;
    }}
    
    /* Header styling */
    h1, h2, h3 {{
        color: {DURABILIS_COLORS['secondary_blue']};
        font-weight: 700;
    }}
    
    /* Custom title banner */
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
    
    /* Section containers */
    .section-container {{
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
        border-left: 4px solid {DURABILIS_COLORS['primary_blue']};
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
    
    /* Form elements */
    .stSelectbox, .stMultiSelect, .stTextInput, .stTextArea {{
        border-radius: 6px;
    }}
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {{
        background-color: #f8f9fa;
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
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .main {{
            padding: 1rem;
        }}
        .platform-title h1 {{
            font-size: 1.8rem;
        }}
    }}
    
    /* Data tables */
    .dataframe {{
        border: 1px solid {DURABILIS_COLORS['light_grey']};
        border-radius: 6px;
    }}
    
    /* Info boxes */
    .stAlert {{
        border-radius: 6px;
    }}
    </style>
    """, unsafe_allow_html=True)

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
# SIDEBAR - Configuration & Data Management
# ============================================================================

st.sidebar.image("/Users/mac/.gemini/antigravity/brain/1efed1ec-870c-4e10-b615-5003352d8c1e/uploaded_image_1768139605245.png", use_container_width=True)
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("---")

# Data source selection
data_mode = st.sidebar.radio(
    "Mode de gestion des données",
    ["📋 Nouveau Projet", "📂 Charger des données", "📊 Voir les projets existants"],
    index=0
)

# ============================================================================
# DATA STORAGE (Session State)
# ============================================================================

if 'projects' not in st.session_state:
    st.session_state.projects = []

# ============================================================================
# MAIN INTERFACE - Structured Sections
# ============================================================================

if data_mode == "📋 Nouveau Projet":
    
    tabs = st.tabs([
        "1️⃣ Informations Générales",
        "2️⃣ Sport & Discipline",
        "3️⃣ Alignement ODD / Agenda 2063",
        "4️⃣ Indicateurs & Suivi"
    ])
    
    # ========================================================================
    # TAB 1: General Information
    # ========================================================================
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
            project_organization = st.text_input("Organisation/Porteur du projet *", placeholder="Ex: Fédération Nationale de Football")
            project_location = st.text_input("Localisation *", placeholder="Ex: Dakar, Région de Thiès")
            project_end_date = st.date_input("Date de fin prévue")
        
        project_description = st.text_area(
            "Description du projet *",
            placeholder="Décrivez brièvement les objectifs et activités du projet RSE...",
            height=120
        )
        
        project_budget = st.number_input("Budget (en €)", min_value=0, step=1000, value=0)
        
        project_beneficiaries = st.number_input("Nombre de bénéficiaires estimés", min_value=0, step=10, value=0)
    
    # ========================================================================
    # TAB 2: Sport & Discipline
    # ========================================================================
    with tabs[1]:
        st.subheader("⚽ Sport & Discipline")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sport_category = st.selectbox(
                "Catégorie de sport *",
                [""] + list(SPORTS_LIST.keys())
            )
            
            if sport_category:
                selected_sports = st.multiselect(
                    "Sélectionner le(s) sport(s) *",
                    SPORTS_LIST[sport_category],
                    help="Vous pouvez sélectionner plusieurs sports"
                )
            else:
                selected_sports = st.multiselect(
                    "Ou rechercher dans tous les sports",
                    ALL_SPORTS,
                    help="Sélectionnez d'abord une catégorie pour un choix plus ciblé"
                )
        
        with col2:
            sport_level = st.multiselect(
                "Niveau de pratique *",
                ["Initiation", "Loisir", "Amateur", "Semi-professionnel", "Professionnel", "Élite/Haut niveau"],
                help="Sélectionnez tous les niveaux concernés"
            )
            
            target_audience = st.multiselect(
                "Public cible *",
                ["Enfants (0-12 ans)", "Adolescents (13-17 ans)", "Jeunes adultes (18-25 ans)", 
                 "Adultes (26-50 ans)", "Seniors (50+ ans)", "Personnes en situation de handicap",
                 "Femmes", "Hommes", "Mixte"],
                help="Sélectionnez tous les publics concernés"
            )
        
        sport_infrastructure = st.text_area(
            "Infrastructures utilisées",
            placeholder="Ex: Stade municipal, Terrain synthétique, Gymnase...",
            height=80
        )
    
    # ========================================================================
    # TAB 3: SDGs & Agenda 2063 Alignment
    # ========================================================================
    with tabs[2]:
        st.subheader("🌍 Alignement ODD (Agenda 2030) & Agenda 2063")
        
        st.markdown("##### 🎯 Objectifs de Développement Durable (ODD)")
        st.info("Sélectionnez les ODD auxquels votre projet contribue directement.")
        
        # Create a grid of SDG checkboxes with visual representation
        sdg_cols = st.columns(3)
        selected_sdgs = []
        
        for idx, sdg in enumerate(SDGS):
            with sdg_cols[idx % 3]:
                sdg_label = f"ODD {sdg['num']}: {sdg['title'][:30]}..."
                if st.checkbox(sdg_label, key=f"sdg_{sdg['num']}"):
                    selected_sdgs.append(f"ODD {sdg['num']}: {sdg['title']}")
        
        st.markdown("---")
        
        st.markdown("##### 🌍 Agenda 2063 de l'Union Africaine")
        st.info("Sélectionnez les aspirations de l'Agenda 2063 alignées avec votre projet.")
        
        selected_agenda_2063 = st.multiselect(
            "Aspirations de l'Agenda 2063",
            AGENDA_2063,
            help="Sélectionnez une ou plusieurs aspirations"
        )
        
        st.markdown("---")
        
        alignment_description = st.text_area(
            "Description de l'alignement stratégique",
            placeholder="Expliquez comment votre projet contribue aux ODD et aspirations sélectionnés...",
            height=100
        )
    
    # ========================================================================
    # TAB 4: Indicators & Monitoring
    # ========================================================================
    with tabs[3]:
        st.subheader("📈 Indicateurs & Suivi")
        
        st.markdown("##### Indicateurs de Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Indicateurs quantitatifs**")
            indicator_participants = st.number_input("Nombre de participants", min_value=0, step=1)
            indicator_sessions = st.number_input("Nombre de sessions/événements", min_value=0, step=1)
            indicator_hours = st.number_input("Heures d'activité totales", min_value=0, step=1)
            
        with col2:
            st.markdown("**Indicateurs qualitatifs**")
            impact_social = st.select_slider(
                "Impact social",
                options=["Très faible", "Faible", "Moyen", "Fort", "Très fort"],
                value="Moyen"
            )
            impact_environmental = st.select_slider(
                "Impact environnemental",
                options=["Très faible", "Faible", "Moyen", "Fort", "Très fort"],
                value="Moyen"
            )
            impact_economic = st.select_slider(
                "Impact économique",
                options=["Très faible", "Faible", "Moyen", "Fort", "Très fort"],
                value="Moyen"
            )
        
        st.markdown("---")
        
        monitoring_tools = st.multiselect(
            "Outils de suivi utilisés",
            ["Questionnaires", "Entretiens", "Observations terrain", "Données analytiques",
             "Reporting mensuel", "Évaluation externe", "Auto-évaluation", "Tableaux de bord"],
            help="Sélectionnez tous les outils utilisés"
        )
        
        monitoring_frequency = st.selectbox(
            "Fréquence de suivi",
            ["Hebdomadaire", "Bimensuel", "Mensuel", "Trimestriel", "Semestriel", "Annuel"]
        )
        
        additional_notes = st.text_area(
            "Notes et commentaires additionnels",
            placeholder="Ajoutez toute information complémentaire pertinente...",
            height=100
        )
    
    # ========================================================================
    # SUBMIT BUTTON
    # ========================================================================
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        submit_button = st.button("💾 Enregistrer le Projet", use_container_width=True, type="primary")
    
    if submit_button:
        # Validation
        if not project_name or not project_organization:
            st.error("❌ Veuillez remplir au minimum le nom du projet et l'organisation.")
        elif not selected_sports:
            st.error("❌ Veuillez sélectionner au moins un sport.")
        else:
            # Create project data
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
            
            # Add to session state
            st.session_state.projects.append(project_data)
            
            st.success(f"✅ Projet '{project_name}' enregistré avec succès!")
            st.balloons()
            
            # Show summary
            with st.expander("📋 Résumé du projet enregistré", expanded=True):
                st.write(f"**Nom:** {project_name}")
                st.write(f"**Organisation:** {project_organization}")
                st.write(f"**Sport(s):** {', '.join(selected_sports)}")
                st.write(f"**ODD sélectionnés:** {len(selected_sdgs)}")
                st.write(f"**Aspirations Agenda 2063:** {len(selected_agenda_2063)}")

# ============================================================================
# LOAD EXISTING DATA MODE
# ============================================================================

elif data_mode == "📂 Charger des données":
    st.subheader("📂 Importer des Données")
    
    uploaded_file = st.file_uploader(
        "Choisir un fichier CSV",
        type=["csv"],
        help="Importez un fichier CSV contenant vos projets RSE"
    )
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Fichier chargé avec succès! {len(df)} projets trouvés.")
            
            st.dataframe(df, use_container_width=True)
            
            # Option to add to session state
            if st.button("Ajouter ces projets à la session"):
                for _, row in df.iterrows():
                    st.session_state.projects.append(row.to_dict())
                st.success("Projets ajoutés à la session!")
                
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement du fichier: {str(e)}")
    
    st.markdown("---")
    st.info("""
    **Format CSV attendu:**
    - Une ligne par projet
    - Colonnes suggerées: name, organization, sports, sdgs, agenda_2063, etc.
    """)

# ============================================================================
# VIEW EXISTING PROJECTS
# ============================================================================

elif data_mode == "📊 Voir les projets existants":
    st.subheader("📊 Projets Enregistrés")
    
    if not st.session_state.projects:
        st.warning("Aucun projet enregistré pour le moment.")
        st.info("👈 Utilisez le mode 'Nouveau Projet' pour ajouter des projets.")
    else:
        st.success(f"**{len(st.session_state.projects)} projet(s) enregistré(s)**")
        
        # Display projects
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
        
        st.markdown("---")
        
        # Export all projects
        if st.button("📥 Exporter tous les projets en CSV"):
            df_export = pd.DataFrame(st.session_state.projects)
            csv = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Télécharger le fichier CSV",
                data=csv,
                file_name=f'projets_rse_sport_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv',
            )

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
