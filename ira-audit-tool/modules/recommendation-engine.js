// Recommendation Engine Module
// Generates personalized action recommendations based on scoring

const RecommendationEngine = {

    // Main function to generate all recommendations
    // @param scores: scoring object from ScoringEngine
    // @param projectProfile: user's project data
    // @return: structured recommendations object
    generateRecommendations(scores, projectProfile) {
        const { weakPrinciples, profile, globalScore } = scores;
        const recommendations = {
            quick: [],     // 0-3 months
            structural: [], // 3-12 months
            strategic: []   // 12+ months
        };

        // Generate recommendations for each weak principle
        weakPrinciples.forEach(principleId => {
            const recs = this.getRecommendationsForPrinciple(
                principleId,
                profile.level,
                projectProfile.activityType
            );

            if (recs.quick) recommendations.quick.push(recs.quick);
            if (recs.structural) recommendations.structural.push(recs.structural);
            if (recs.strategic) recommendations.strategic.push(recs.strategic);
        });

        // Prioritize and limit recommendations
        return {
            quick: this.prioritizeActions(recommendations.quick).slice(0, 3),
            structural: this.prioritizeActions(recommendations.structural).slice(0, 2),
            strategic: this.prioritizeActions(recommendations.strategic).slice(0, 1)
        };
    },

    // Get recommendations for a specific principle
    // @param principleId: 1-10
    // @param profileLevel: A, B, C, or D
    // @param activityType: elevage, culture, transformation, mixte
    // @return: object with quick, structural, strategic actions
    getRecommendationsForPrinciple(principleId, profileLevel, activityType) {
        const principle = CSA_IRA_QUESTIONS.principles.find(p => p.id === principleId);
        if (!principle) return {};

        const commonActions = this.getCommonActions(principleId);
        const specificActions = this.getActivitySpecificActions(principleId, activityType);

        return {
            quick: {
                principleId,
                principleName: principle.title,
                icon: principle.icon,
                ...commonActions.quick,
                ...specificActions.quick
            },
            structural: {
                principleId,
                principleName: principle.title,
                icon: principle.icon,
                ...commonActions.structural,
                ...specificActions.structural
            },
            strategic: {
                principleId,
                principleName: principle.title,
                icon: principle.icon,
                ...commonActions.strategic,
                ...specificActions.strategic
            }
        };
    },

    // Common actions for each principle (applicable to all)
    getCommonActions(principleId) {
        const actions = {
            1: { // Sécurité alimentaire
                quick: {
                    title: "Identifier les besoins alimentaires locaux",
                    description: "Discute avec ta communauté pour savoir quels aliments sont les plus recherchés",
                    impact: "+0.25 au principe 1"
                },
                structural: {
                    title: "Diversifier pour mieux nourrir",
                    description: "Ajoute une culture ou un élevage complémentaire pour assurer une alimentation variée",
                    impact: "Améliore principes 1 et 6"
                },
                strategic: {
                    title: "Créer un circuit court alimentaire",
                    description: "Organise un système de vente directe ou rejoins une coopérative locale",
                    impact: "Améliore principes 1, 2 et 9"
                }
            },
            2: { // Développement économique
                quick: {
                    title: "Tenir un registre simple des revenus",
                    description: "Note tes ventes et dépenses dans un cahier ou sur ton téléphone",
                    impact: "+0.25 au principe 2"
                },
                structural: {
                    title: "Créer de la valeur ajoutée",
                    description: "Transforme une partie de ta production (séchage, conservation, emballage)",
                    impact: "Améliore principes 2 et 8"
                },
                strategic: {
                    title: "Développer un partenariat commercial",
                    description: "Trouve un transformateur ou vendeur local pour sécuriser tes débouchés",
                    impact: "+10% score global"
                }
            },
            3: { // Égalité femmes-hommes
                quick: {
                    title: "Impliquer les femmes dans les décisions",
                    description: "Organise une réunion où les femmes peuvent s'exprimer sur le projet",
                    impact: "+0.25 au principe 3"
                },
                structural: {
                    title: "Assurer l'équité salariale",
                    description: "Écris et partage des règles claires : même travail, même salaire",
                    impact: "Améliore principes 3 et 9"
                },
                strategic: {
                    title: "Former et autonomiser les femmes",
                    description: "Mets en place un programme de formation pour renforcer les compétences",
                    impact: "Améliore principes 3 et 4"
                }
            },
            4: { // Jeunes et autonomisation
                quick: {
                    title: "Confier des responsabilités aux jeunes",
                    description: "Donne à un jeune la gestion d'une parcelle ou d'une activité spécifique",
                    impact: "+0.25 au principe 4"
                },
                structural: {
                    title: "Organiser des sessions de formation",
                    description: "Forme les jeunes à de nouvelles techniques ou à la gestion",
                    impact: "Améliore principes 4 et 7"
                },
                strategic: {
                    title: "Créer un programme de mentorat",
                    description: "Accompagne des jeunes agriculteurs avec ton expérience",
                    impact: "Améliore principes 4, 9 et 10"
                }
            },
            5: { // Régimes fonciers
                quick: {
                    title: "Clarifier l'accès aux ressources",
                    description: "Discute avec les propriétaires/autorités pour sécuriser ton accès à la terre",
                    impact: "+0.25 au principe 5"
                },
                structural: {
                    title: "Formaliser les droits d'usage",
                    description: "Obtiens un document écrit (contrat, accord) sur l'utilisation de la terre",
                    impact: "Améliore principes 5 et 9"
                },
                strategic: {
                    title: "Négocier un bail à long terme",
                    description: "Sécurise ton accès à la terre pour au moins 5-10 ans",
                    impact: "+15% score global"
                }
            },
            6: { // Ressources naturelles
                quick: {
                    title: "Adopter une pratique éco-responsable",
                    description: "Ex: compostage, récupération d'eau de pluie, mulching",
                    impact: "+0.25 au principe 6"
                },
                structural: {
                    title: "Mettre en place une rotation des cultures",
                    description: "Alterner les cultures pour préserver la fertilité du sol",
                    impact: "Améliore principes 6 et 1"
                },
                strategic: {
                    title: "Adopter l'agroécologie",
                    description: "Intègre plusieurs pratiques durables : agroforesterie, associations de cultures",
                    impact: "+20% score global"
                }
            },
            7: { // Patrimoine culturel
                quick: {
                    title: "Valoriser une pratique traditionnelle",
                    description: "Identifie et réintroduis une technique ou variété locale",
                    impact: "+0.25 au principe 7"
                },
                structural: {
                    title: "Combiner tradition et innovation",
                    description: "Associe des savoirs ancestraux avec des outils modernes",
                    impact: "Améliore principes 7 et 4"
                },
                strategic: {
                    title: "Devenir gardien de la biodiversité locale",
                    description: "Conserve et multiplie des semences ou races traditionnelles",
                    impact: "Améliore principes 7, 6 et 8"
                }
            },
            8: { // Systèmes alimentaires sûrs
                quick: {
                    title: "Améliorer l'hygiène de base",
                    description: "Nettoie les outils, lave les produits, stocke dans un endroit propre",
                    impact: "+0.25 au principe 8"
                },
                structural: {
                    title: "Améliorer le stockage et la transformation",
                    description: "Utilise des contenants propres et adaptés, évite les contaminations",
                    impact: "Améliore principes 8 et 2"
                },
                strategic: {
                    title: "Obtenir une certification qualité",
                    description: "Vise une certification locale ou bio pour valoriser tes produits",
                    impact: "+15% score global"
                }
            },
            9: { // Gouvernance
                quick: {
                    title: "Écrire 3 règles simples",
                    description: "Note les règles de base : partage des revenus, horaires, responsabilités",
                    impact: "+0.25 au principe 9"
                },
                structural: {
                    title: "Organiser des réunions régulières",
                    description: "Fixe un moment mensuel pour discuter avec tous les participants",
                    impact: "Améliore principes 9 et 3"
                },
                strategic: {
                    title: "Créer une structure formelle",
                    description: "Transforme ton projet en coopérative ou association",
                    impact: "+20% score global"
                }
            },
            10: { // Suivi et impacts
                quick: {
                    title: "Commencer un suivi simple",
                    description: "Note chaque semaine : production, ventes, activités réalisées",
                    impact: "+0.25 au principe 10"
                },
                structural: {
                    title: "Mesurer 3 indicateurs clés",
                    description: "Suis régulièrement : revenus, emplois créés, ressources utilisées",
                    impact: "Améliore principes 10 et 2"
                },
                strategic: {
                    title: "Produire un rapport d'impact annuel",
                    description: "Documente tes résultats économiques, sociaux et environnementaux",
                    impact: "Préparation investissement"
                }
            }
        };

        return actions[principleId] || {};
    },

    // Activity-specific actions (tailored to project type)
    getActivitySpecificActions(principleId, activityType) {
        // Activity-specific nuances can be added here
        // For now, returning empty object (common actions are sufficient)
        return {
            quick: {},
            structural: {},
            strategic: {}
        };
    },

    // Prioritize actions by impact and feasibility
    prioritizeActions(actions) {
        return actions.sort((a, b) => {
            // Prioritize by number of principles impacted (multi-impact actions first)
            const impactA = (a.impact.match(/principes/g) || []).length;
            const impactB = (b.impact.match(/principes/g) || []).length;
            return impactB - impactA;
        });
    },

    // Generate explanation for weak principle
    getWeakPrincipleExplanation(principleId) {
        const explanations = {
            1: "Ce principe est faible car ton projet ne contribue pas encore suffisamment à l'alimentation locale.",
            2: "Ce principe est faible car la création de valeur économique locale est limitée.",
            3: "Ce principe est faible car la participation des femmes n'est pas encore pleinement assurée.",
            4: "Ce principe est faible car les jeunes ne sont pas assez impliqués ou formés.",
            5: "Ce principe est faible car l'accès aux ressources (terre, eau) n'est pas clairement sécurisé.",
            6: "Ce principe est faible car les pratiques de préservation des ressources naturelles sont insuffisantes.",
            7: "Ce principe est faible car les savoirs traditionnels ne sont pas valorisés.",
            8: "Ce principe est faible car la qualité et la sécurité des produits ne sont pas assez formalisées.",
            9: "Ce principe est faible car les règles de gouvernance ne sont pas claires pour tous.",
            10: "Ce principe est faible car le suivi des impacts n'est pas mis en place."
        };

        return explanations[principleId] || "Ce principe nécessite un renforcement.";
    }
};
