// Case Studies Data
// Inspirational examples: Mohamed & Fadi, and Inès

const CASE_STUDIES = {
    mohamedFadi: {
        id: "mohamed-fadi",
        title: "Mohamed & Fadi : Élevage + Transformation locale",
        label: "Exemple inspirant",
        activityTypes: ["elevage", "transformation", "mixte"],
        weakPrinciples: [7, 8, 2], // Patrimoine culturel, Systèmes alimentaires, Développement économique
        description: "Mohamed (éleveur) et Fadi (fromager) ont renforcé leur projet en travaillant ensemble : production + transformation + vente locale.",
        imageUrl: "assets/images/case-mohamed-fadi.jpg",
        whatTheyDid: [
            "Valorisation d'une race laitière locale adaptée au climat",
            "Création d'une fromagerie artisanale avec matériaux naturels",
            "Partenariat producteur-transformateur pour assurer des débouchés",
            "Formation de 3 jeunes aux techniques de transformation",
            "Vente directe sur les marchés locaux"
        ],
        whatYouCanDo: [
            "Identifier un partenaire local (transformateur, commerçant)",
            "Valoriser une race ou variété locale de ton terroir",
            "Améliorer l'emballage ou la présentation de tes produits",
            "Commencer par une transformation simple (séchage, conserves)",
            "Créer un point de vente direct ou rejoindre un marché"
        ],
        impact: {
            principles: [2, 7, 8],
            score_increase: "+15 à +20 points IRA"
        }
    },
    ines: {
        id: "ines",
        title: "Inès : Agriculture intégrée et savoirs traditionnels",
        label: "Exemple inspirant",
        activityTypes: ["culture", "mixte"],
        weakPrinciples: [6, 9, 7], // Ressources naturelles, Gouvernance, Patrimoine culturel
        description: "Inès combine pratiques traditionnelles (jarres romaines, savoirs familiaux) et innovations modernes. Elle respecte l'égalité salariale et anticipe les impacts climatiques.",
        imageUrl: "assets/images/case-ines.jpg",
        whatTheyDid: [
            "Utilisation de techniques ancestrales de conservation de l'eau (jarres)",
            "Association de cultures traditionnelles et modernes",
            "Mise en place de règles claires : rémunération égale femmes-hommes",
            "Rotation des cultures pour préserver les sols",
            "Système simple de suivi des rendements et de l'impact environnemental"
        ],
        whatYouCanDo: [
            "Intégrer une pratique traditionnelle locale dans ton exploitation",
            "Améliorer la gestion de l'eau (récupération, irrigation efficiente)",
            "Clarifier les règles de travail et de rémunération",
            "Alterner les cultures pour ne pas épuiser les sols",
            "Tenir un cahier simple pour suivre tes activités"
        ],
        impact: {
            principles: [6, 7, 9],
            score_increase: "+12 à +18 points IRA"
        }
    }
};

// Function to get relevant case study based on project profile and weak principles
function getRelevantCaseStudy(activityType, weakPrinciples) {
    const mohamedScore = calculateCaseRelevance(
        CASE_STUDIES.mohamedFadi,
        activityType,
        weakPrinciples
    );
    const inesScore = calculateCaseRelevance(
        CASE_STUDIES.ines,
        activityType,
        weakPrinciples
    );

    // Return the most relevant case study
    return mohamedScore >= inesScore
        ? CASE_STUDIES.mohamedFadi
        : CASE_STUDIES.ines;
}

function calculateCaseRelevance(caseStudy, activityType, weakPrinciples) {
    let score = 0;

    // Check activity type match
    if (caseStudy.activityTypes.includes(activityType)) {
        score += 10;
    }

    // Check weak principles overlap
    const overlap = weakPrinciples.filter(p =>
        caseStudy.weakPrinciples.includes(p)
    );
    score += overlap.length * 5;

    return score;
}
