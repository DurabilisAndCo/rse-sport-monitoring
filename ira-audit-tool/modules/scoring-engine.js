// Scoring Engine Module
// Calculates scores for CSA-IRA assessment

const ScoringEngine = {

    // Calculate score for a single question
    // @param value: 0, 0.5, or 1
    // @return: question score
    calculateQuestionScore(value) {
        return parseFloat(value);
    },

    // Calculate score for a principle (average of questions)
    // @param questionScores: array of question scores
    // @return: principle score (0 to 1)
    calculatePrincipleScore(questionScores) {
        if (!questionScores || questionScores.length === 0) return 0;
        const sum = questionScores.reduce((acc, score) => acc + score, 0);
        return sum / questionScores.length;
    },

    // Calculate global score (average of all principles)
    // @param principleScores: array of principle scores
    // @return: global score as percentage (0 to 100)
    calculateGlobalScore(principleScores) {
        if (!principleScores || principleScores.length === 0) return 0;
        const sum = principleScores.reduce((acc, score) => acc + score, 0);
        const average = sum / principleScores.length;
        return Math.round(average * 100);
    },

    // Classify project profile based on global score
    // @param globalScore: score percentage (0-100)
    // @return: profile object { level, name, color, icon, message }
    classifyProfile(globalScore) {
        if (globalScore < 30) {
            return {
                level: 'A',
                name: 'Projet en phase de structuration',
                color: 'hsl(0, 84%, 60%)',
                icon: '🔴',
                message: 'Ton projet a du potentiel, mais il manque encore des bases pour accéder à un investissement responsable. Concentre-toi sur les fondamentaux.',
                objective: 'Sécuriser les fondamentaux et poser les premières pratiques responsables',
                nextPhase: 'Atteindre 30% pour passer en phase de transition'
            };
        } else if (globalScore >= 30 && globalScore < 50) {
            return {
                level: 'B',
                name: 'Projet en transition vers l\'IRA',
                color: 'hsl(38, 92%, 50%)',
                icon: '🟠',
                message: 'Ton projet commence à intégrer des pratiques responsables, mais elles sont encore incomplètes ou informelles. Quelques actions ciblées te permettront de franchir le seuil IRA.',
                objective: 'Formaliser les pratiques existantes et atteindre le seuil des 50%',
                nextPhase: 'Atteindre 50% pour devenir éligible IRA'
            };
        } else if (globalScore >= 50 && globalScore < 70) {
            return {
                level: 'C',
                name: 'Projet potentiellement éligible IRA',
                color: 'hsl(85, 85%, 50%)',
                icon: '🟢',
                message: 'Ton projet est globalement aligné avec l\'investissement agricole responsable. Continue à consolider et à documenter tes pratiques.',
                objective: 'Consolider, documenter et se préparer à dialoguer avec un financeur',
                nextPhase: 'Atteindre 70% pour devenir projet exemplaire'
            };
        } else {
            return {
                level: 'D',
                name: 'Projet exemplaire IRA',
                color: 'hsl(142, 71%, 45%)',
                icon: '🌿',
                message: 'Ton projet peut servir de référence et inspirer d\'autres jeunes agriculteurs. Tu es prêt pour l\'investissement responsable.',
                objective: 'Valoriser ton projet et accéder au financement',
                nextPhase: 'Rechercher activement des investisseurs responsables'
            };
        }
    },

    // Identify weak principles (score < threshold)
    // @param principleScores: array of { id, score } objects
    // @param threshold: minimum score (default 0.5)
    // @return: array of weak principle IDs
    identifyWeakPrinciples(principleScores, threshold = 0.5) {
        return principleScores
            .filter(p => p.score < threshold)
            .map(p => p.id)
            .sort((a, b) => {
                const scoreA = principleScores.find(p => p.id === a).score;
                const scoreB = principleScores.find(p => p.id === b).score;
                return scoreA - scoreB; // Sort by weakest first
            });
    },

    // Identify strong principles (score >= threshold)
    // @param principleScores: array of { id, score } objects
    // @param threshold: minimum score (default 0.75)
    // @return: array of strong principle IDs
    identifyStrongPrinciples(principleScores, threshold = 0.75) {
        return principleScores
            .filter(p => p.score >= threshold)
            .map(p => p.id)
            .sort((a, b) => {
                const scoreA = principleScores.find(p => p.id === a).score;
                const scoreB = principleScores.find(p => p.id === b).score;
                return scoreB - scoreA; // Sort by strongest first
            });
    },

    // Get color for score visualization
    // @param score: score value (0-100 for global, 0-1 for principle)
    // @param isPercentage: whether score is already percentage
    // @return: HSL color string
    getScoreColor(score, isPercentage = false) {
        const percent = isPercentage ? score : score * 100;

        if (percent < 30) {
            return 'hsl(0, 84%, 60%)'; // Red
        } else if (percent < 50) {
            return 'hsl(38, 92%, 50%)'; // Orange
        } else if (percent < 70) {
            return 'hsl(85, 85%, 50%)'; // Yellow-green
        } else {
            return 'hsl(142, 71%, 45%)'; // Green
        }
    },

    // Calculate all scores from assessment responses
    // @param responses: object with principle responses { p1: [0.5, 1], p2: [1, 0.5], ... }
    // @return: complete scoring object
    calculateAllScores(responses) {
        const principleScores = [];

        // Calculate each principle score
        for (let i = 1; i <= 10; i++) {
            const principleKey = `p${i}`;
            const questionScores = responses[principleKey] || [];
            const score = this.calculatePrincipleScore(questionScores);
            principleScores.push({ id: i, score });
        }

        // Calculate global score
        const globalScore = this.calculateGlobalScore(
            principleScores.map(p => p.score)
        );

        // Classify profile
        const profile = this.classifyProfile(globalScore);

        // Identify weak and strong principles
        const weakPrinciples = this.identifyWeakPrinciples(principleScores);
        const strongPrinciples = this.identifyStrongPrinciples(principleScores);

        return {
            globalScore,
            profile,
            principleScores,
            weakPrinciples,
            strongPrinciples
        };
    }
};
