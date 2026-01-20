// CSA-IRA Questions Data
// 10 Principles with 2-3 questions each

const CSA_IRA_QUESTIONS = {
    principles: [
        {
            id: 1,
            number: "Principe 1",
            title: "Sécurité alimentaire et nutrition",
            icon: "🍚",
            color: "hsl(142, 71%, 45%)",
            description: "Contribution à l'alimentation locale de qualité",
            questions: [
                {
                    id: "p1q1",
                    text: "Le projet contribue-t-il à fournir des aliments utiles et accessibles aux populations locales ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                },
                {
                    id: "p1q2",
                    text: "Les produits sont-ils destinés à l'alimentation humaine ou animale de qualité ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                }
            ]
        },
        {
            id: 2,
            number: "Principe 2",
            title: "Développement économique durable et inclusif",
            icon: "💰",
            color: "hsl(200, 71%, 45%)",
            description: "Création de valeur locale et revenus durables",
            questions: [
                {
                    id: "p2q1",
                    text: "Le projet génère-t-il des revenus réguliers et prévisibles ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                },
                {
                    id: "p2q2",
                    text: "Le projet crée-t-il de la valeur localement (emplois, services, transformation) ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                }
            ]
        },
        {
            id: 3,
            number: "Principe 3",
            title: "Égalité femmes-hommes",
            icon: "⚖️",
            color: "hsl(330, 71%, 45%)",
            description: "Participation et équité pour les femmes",
            questions: [
                {
                    id: "p3q1",
                    text: "Les femmes participent-elles activement au projet ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                },
                {
                    id: "p3q2",
                    text: "Les conditions de travail et de rémunération sont-elles équitables ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                }
            ]
        },
        {
            id: 4,
            number: "Principe 4",
            title: "Jeunes et autonomisation",
            icon: "🧑‍🌾",
            color: "hsl(40, 90%, 50%)",
            description: "Implication et formation des jeunes",
            questions: [
                {
                    id: "p4q1",
                    text: "Des jeunes sont-ils impliqués dans les décisions ou les opérations ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                },
                {
                    id: "p4q2",
                    text: "Le projet favorise-t-il l'apprentissage, la formation ou l'innovation des jeunes ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                }
            ]
        },
        {
            id: 5,
            number: "Principe 5",
            title: "Régimes fonciers et accès aux ressources",
            icon: "🌍",
            color: "hsl(25, 75%, 45%)",
            description: "Sécurisation de l'accès aux ressources",
            questions: [
                {
                    id: "p5q1",
                    text: "L'accès à la terre et à l'eau est-il clair, sécurisé et non conflictuel ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                },
                {
                    id: "p5q2",
                    text: "Le projet respecte-t-il les usages locaux et les droits existants ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                }
            ]
        },
        {
            id: 6,
            number: "Principe 6",
            title: "Ressources naturelles et résilience climatique",
            icon: "🌱",
            color: "hsl(120, 60%, 40%)",
            description: "Pratiques durables et adaptation climatique",
            questions: [
                {
                    id: "p6q1",
                    text: "Les pratiques agricoles préservent-elles les sols, l'eau et la biodiversité ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                },
                {
                    id: "p6q2",
                    text: "Le projet tient-il compte des risques climatiques (sécheresse, chaleur, maladies) ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                }
            ]
        },
        {
            id: 7,
            number: "Principe 7",
            title: "Patrimoine culturel et savoirs traditionnels",
            icon: "📚",
            color: "hsl(280, 60%, 50%)",
            description: "Valorisation des savoirs locaux",
            questions: [
                {
                    id: "p7q1",
                    text: "Le projet valorise-t-il des savoir-faire, races, semences ou pratiques locales ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                },
                {
                    id: "p7q2",
                    text: "Ces savoirs sont-ils combinés à des innovations utiles ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                }
            ]
        },
        {
            id: 8,
            number: "Principe 8",
            title: "Systèmes alimentaires sûrs et sains",
            icon: "🏥",
            color: "hsl(15, 80%, 50%)",
            description: "Qualité et sécurité des produits",
            questions: [
                {
                    id: "p8q1",
                    text: "Les produits sont-ils sains, sûrs et transformés dans de bonnes conditions ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                },
                {
                    id: "p8q2",
                    text: "Des pratiques d'hygiène ou de qualité sont-elles mises en place (même simples) ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                }
            ]
        },
        {
            id: 9,
            number: "Principe 9",
            title: "Gouvernance et transparence",
            icon: "👥",
            color: "hsl(210, 70%, 45%)",
            description: "Règles claires et dialogue",
            questions: [
                {
                    id: "p9q1",
                    text: "Les règles du projet sont-elles claires pour tous les participants ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                },
                {
                    id: "p9q2",
                    text: "Existe-t-il des mécanismes simples de dialogue ou de résolution des conflits ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                }
            ]
        },
        {
            id: 10,
            number: "Principe 10",
            title: "Suivi, impacts et responsabilité",
            icon: "📊",
            color: "hsl(180, 60%, 40%)",
            description: "Mesure et redevabilité",
            questions: [
                {
                    id: "p10q1",
                    text: "Le projet suit-il ses impacts (économiques, sociaux, environnementaux) ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                },
                {
                    id: "p10q2",
                    text: "Le porteur du projet est-il prêt à rendre compte de ses pratiques ?",
                    answers: [
                        { value: 0, icon: "❌", text: "Pas encore" },
                        { value: 0.5, icon: "⚠️", text: "En partie" },
                        { value: 1, icon: "✅", text: "Oui" }
                    ]
                }
            ]
        }
    ]
};
