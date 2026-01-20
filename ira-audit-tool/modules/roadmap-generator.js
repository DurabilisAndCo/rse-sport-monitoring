// Roadmap Generator Module
// Creates personalized roadmap based on current score and profile

const RoadmapGenerator = {

    // Generate complete roadmap
    // @param scores: scoring object from ScoringEngine
    // @return: roadmap object with phases and timeline
    generateRoadmap(scores) {
        const { globalScore, profile } = scores;

        const phases = this.getAllPhases();
        const currentPhase = this.getCurrentPhase(globalScore);
        const nextMilestone = this.getNextMilestone(globalScore);
        const timeline = this.generateTimeline(globalScore);

        return {
            currentPhase,
            nextMilestone,
            phases,
            timeline,
            estimatedDuration: this.estimateTimeToTarget(globalScore, 50)
        };
    },

    // Get all roadmap phases
    getAllPhases() {
        return [
            {
                id: 0,
                name: "Poser les bases",
                scoreRange: "< 30%",
                duration: "0-3 mois",
                color: "hsl(0, 84%, 60%)",
                icon: "🔴",
                objectives: [
                    "Sécuriser les fondamentaux",
                    "Éviter les risques majeurs",
                    "Poser les premières pratiques responsables"
                ],
                keyActions: [
                    "Clarifier ton activité et tes objectifs",
                    "Sécuriser l'accès aux ressources de base",
                    "Définir 3 règles simples de fonctionnement"
                ]
            },
            {
                id: 1,
                name: "Passer le seuil IRA",
                scoreRange: "30-49%",
                duration: "3-6 mois",
                color: "hsl(38, 92%, 50%)",
                icon: "🟠",
                objectives: [
                    "Atteindre 50% minimum",
                    "Formaliser les pratiques existantes",
                    "Renforcer 2-3 principes clés"
                ],
                keyActions: [
                    "Documenter ce qui était informel",
                    "Commencer un suivi simple",
                    "S'inspirer d'exemples concrets"
                ]
            },
            {
                id: 2,
                name: "Consolider & crédibiliser",
                scoreRange: "50-69%",
                duration: "6-9 mois",
                color: "hsl(85, 85%, 50%)",
                icon: "🟢",
                objectives: [
                    "Rendre le projet lisible pour un financeur",
                    "Réduire les risques",
                    "Préparer le dialogue investissement"
                ],
                keyActions: [
                    "Documenter toutes les pratiques responsables",
                    "Mesurer 3 indicateurs d'impact",
                    "Structurer la gouvernance"
                ]
            },
            {
                id: 3,
                name: "Valoriser & investir",
                scoreRange: "≥ 70%",
                duration: "9-12 mois",
                color: "hsl(142, 71%, 45%)",
                icon: "🌿",
                objectives: [
                    "Accéder à un financement responsable",
                    "Devenir projet vitrine",
                    "Inspirer d'autres agriculteurs"
                ],
                keyActions: [
                    "Préparer le dossier investissement",
                    "Explorer les leviers financiers",
                    "Partager ton expérience"
                ]
            }
        ];
    },

    // Determine current phase based on score
    getCurrentPhase(globalScore) {
        if (globalScore < 30) return 0;
        if (globalScore < 50) return 1;
        if (globalScore < 70) return 2;
        return 3;
    },

    // Get next milestone to reach
    getNextMilestone(globalScore) {
        if (globalScore < 30) {
            return {
                target: 30,
                label: "Atteindre 30% pour passer en transition IRA",
                pointsNeeded: 30 - globalScore
            };
        } else if (globalScore < 50) {
            return {
                target: 50,
                label: "Atteindre 50% pour devenir éligible IRA",
                pointsNeeded: 50 - globalScore
            };
        } else if (globalScore < 70) {
            return {
                target: 70,
                label: "Atteindre 70% pour devenir projet exemplaire",
                pointsNeeded: 70 - globalScore
            };
        } else {
            return {
                target: 100,
                label: "Maintenir l'excellence et chercher financement",
                pointsNeeded: 0
            };
        }
    },

    // Generate visual timeline
    generateTimeline(globalScore) {
        const phases = this.getAllPhases();
        const currentPhaseIndex = this.getCurrentPhase(globalScore);

        return phases.map((phase, index) => ({
            ...phase,
            isActive: index === currentPhaseIndex,
            isCompleted: index < currentPhaseIndex,
            isFuture: index > currentPhaseIndex
        }));
    },

    // Estimate time needed to reach target score
    // Assumes ~5-10 points improvement per month with active work
    estimateTimeToTarget(currentScore, targetScore) {
        if (currentScore >= targetScore) {
            return { months: 0, message: "Objectif atteint !" };
        }

        const pointsNeeded = targetScore - currentScore;
        const monthsNeeded = Math.ceil(pointsNeeded / 7.5); // Average 7.5 points/month

        return {
            months: monthsNeeded,
            message: `Environ ${monthsNeeded} mois avec les actions prioritaires`
        };
    },

    // Get personalized objective message
    getObjectiveMessage(profile, nextMilestone) {
        const messages = {
            'A': `Concentre-toi sur les fondamentaux. Tu dois gagner ${nextMilestone.pointsNeeded} points pour passer en transition IRA.`,
            'B': `Tu es sur la bonne voie ! Encore ${nextMilestone.pointsNeeded} points pour atteindre le seuil d'éligibilité IRA (50%).`,
            'C': `Bravo, ton projet est aligné IRA ! Continue à consolider pour devenir exemplaire (${nextMilestone.pointsNeeded} points restants).`,
            'D': `Excellent ! Ton projet est exemplaire. Tu es prêt à rechercher activement des investisseurs responsables.`
        };

        return messages[profile.level] || messages['A'];
    },

    // Get recommended focus areas based on phase
    getFocusAreas(phase) {
        const focusMap = {
            0: ["Principe 5 (Régimes fonciers)", "Principe 9 (Gouvernance)", "Principe 2 (Revenus)"],
            1: ["Principe 6 (Ressources naturelles)", "Principe 4 (Jeunes)", "Principe 8 (Qualité)"],
            2: ["Principe 10 (Suivi impacts)", "Principe 7 (Patrimoine culturel)", "Principe 3 (Égalité genre)"],
            3: ["Valorisation", "Financement", "Mentorat"]
        };

        return focusMap[phase] || [];
    }
};
