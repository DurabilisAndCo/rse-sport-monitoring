import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# Configuration de la page
st.set_page_config(
    page_title="Matrice de Matérialité RSE - Sport",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Style CSS personnalisé pour l'optimisation UX/UI et responsive
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stPlotlyChart {
        width: 100% !important;
    }
    @media (max-width: 640px) {
        .main {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Fonction pour charger les données
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        try:
            df = pd.read_csv("data.csv")
        except FileNotFoundError:
            st.error("Fichier de données par défaut (data.csv) non trouvé.")
            df = pd.DataFrame(columns=["Enjeu", "Catégorie", "Importance_Entreprise", "Importance_Parties_Prenantes", "Alignement_ODD", "Alignement_Agenda_2063"])
    return df

# Sidebar - Filtres et Options
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("---")

# Option de saisie de données
st.sidebar.subheader("📥 Saisie des Données")
data_source = st.sidebar.radio(
    "Choisissez la source des données:",
    ("Utiliser les données par défaut", "Uploader un fichier CSV", "Saisie manuelle")
)

df = pd.DataFrame()

if data_source == "Uploader un fichier CSV":
    uploaded_file = st.sidebar.file_uploader("Uploader votre fichier CSV", type=["csv"])
    if uploaded_file:
        df = load_data(uploaded_file)
    else:
        st.info("Veuillez uploader un fichier CSV pour continuer.")
elif data_source == "Saisie manuelle":
    st.sidebar.markdown("--- \n **Ajouter un nouvel enjeu**")
    with st.sidebar.form("new_issue_form"):
        enjeu = st.text_input("Enjeu")
        categorie = st.selectbox("Catégorie", ["Environnement", "Social", "Gouvernance", "Business", "Autre"])
        importance_entreprise = st.slider("Importance pour l'Entreprise", 0, 10, 5)
        importance_parties_prenantes = st.slider("Importance pour les Parties Prenantes", 0, 10, 5)
        alignement_odd = st.text_input("Alignement ODD (ex: ODD 13)")
        alignement_agenda_2063 = st.text_input("Alignement Agenda 2063 (ex: Aspiration 1)")
        submitted = st.form_submit_button("Ajouter l'enjeu")
        
        if submitted:
            new_data = pd.DataFrame([{
                "Enjeu": enjeu,
                "Catégorie": categorie,
                "Importance_Entreprise": importance_entreprise,
                "Importance_Parties_Prenantes": importance_parties_prenantes,
                "Alignement_ODD": alignement_odd,
                "Alignement_Agenda_2063": alignement_agenda_2063
            }])
            # Charger les données existantes pour les concaténer
            existing_df = load_data() # Charge les données par défaut si pas d'upload
            df = pd.concat([existing_df, new_data], ignore_index=True)
            st.sidebar.success("Enjeu ajouté avec succès!")
            st.experimental_rerun() # Pour rafraîchir le dashboard avec les nouvelles données
else:
    df = load_data() # Utiliser les données par défaut


# Vérifier si le DataFrame est vide avant de continuer
if df.empty:
    st.warning("Aucune donnée à afficher. Veuillez uploader un fichier, saisir des données manuellement ou utiliser les données par défaut.")
    st.stop()

# Mode d'affichage (Simulé car Streamlit gère le light/dark nativement via les paramètres système)
st.sidebar.info("L'application s'adapte automatiquement au mode clair/sombre de votre système.")

# Filtres
categories = st.sidebar.multiselect(
    "Filtrer par Catégorie",
    options=df["Catégorie"].unique(),
    default=df["Catégorie"].unique()
)

filtered_df = df[df["Catégorie"].isin(categories)]

# Titre principal
st.title("📊 Matrice de Matérialité RSE & Sport")
st.markdown("""
Cette application permet de visualiser et de prioriser les enjeux clés de la Responsabilité Sociétale des Entreprises (RSE) dans le secteur du sport. 
Elle aligne les objectifs business avec les **Objectifs de Développement Durable (ODD)** et l'**Agenda 2063**.
""")

# Layout principal
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Visualisation de la Matrice")
    
    # Création du graphique de matérialité avec Plotly
    fig = px.scatter(
        filtered_df,
        x="Importance_Entreprise",
        y="Importance_Parties_Prenantes",
        text="Enjeu",
        color="Catégorie",
        size=[15]*len(filtered_df) if not filtered_df.empty else [15], # Assurer une taille même si filtered_df est vide
        hover_data=["Alignement_ODD", "Alignement_Agenda_2063"],
        labels={
            "Importance_Entreprise": "Importance pour l'Entreprise (Business)",
            "Importance_Parties_Prenantes": "Importance pour les Parties Prenantes"
        },
        range_x=[0, 11],
        range_y=[0, 11],
        template="plotly_white"
    )

    # Ajouter des lignes de quadrants
    fig.add_shape(type="line", x0=5, y0=0, x1=5, y1=11, line=dict(color="Gray", dash="dash"))
    fig.add_shape(type="line", x0=0, y0=5, x1=11, y1=5, line=dict(color="Gray", dash="dash"))

    # Annotations des quadrants
    fig.add_annotation(x=2.5, y=10.5, text="À surveiller", showarrow=False, font=dict(color="gray"))
    fig.add_annotation(x=8.5, y=10.5, text="Priorités Stratégiques", showarrow=False, font=dict(color="red", size=14))
    fig.add_annotation(x=2.5, y=0.5, text="Faible impact", showarrow=False, font=dict(color="gray"))
    fig.add_annotation(x=8.5, y=0.5, text="Opérationnel", showarrow=False, font=dict(color="gray"))

    fig.update_traces(textposition='top center')
    fig.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Détails des Enjeux")
    st.dataframe(
        filtered_df[["Enjeu", "Catégorie", "Alignement_ODD"]],
        use_container_width=True,
        hide_index=True
    )
    
    st.info("""
    **Légende des Quadrants :**
    - **Priorités Stratégiques :** Enjeux cruciaux pour tous.
    - **À surveiller :** Attentes fortes des parties prenantes.
    - **Opérationnel :** Important pour le business mais moins visible.
    """)
    
    # Bouton d'exportation
    st.subheader("📤 Exporter les Données")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Télécharger les données en CSV",
        data=csv,
        file_name='matrice_materialite_rse_sport.csv',
        mime='text/csv',
    )

# Section Alignement International
st.markdown("---")
st.subheader("🌍 Alignement Stratégique (ODD & Agenda 2063)")

# Afficher les expanders uniquement si filtered_df n'est pas vide
if not filtered_df.empty:
    odd_cols = st.columns(3)
    for i, (idx, row) in enumerate(filtered_df.iterrows()):
        with odd_cols[i % 3]:
            with st.expander(f"🔍 {row['Enjeu']}"):
                st.write(f"**Catégorie:** {row['Catégorie']}")
                st.write(f"**Alignement ODD:** {row['Alignement_ODD']}")
                st.write(f"**Agenda 2063:** {row['Alignement_Agenda_2063']}")
else:
    st.info("Aucun enjeu sélectionné ou disponible pour afficher les détails d'alignement.")

# Footer
st.markdown("---")
st.markdown("💻 Développé pour une utilisation sur Mobile, Tablette et Desktop.")
