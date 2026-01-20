// Main Application Controller
// Orchestrates all modules and manages app state

const app = {
    // Application state
    state: {
        currentScreen: 0,
        currentPrinciple: 0,
        projectProfile: {},
        assessmentResponses: {},
        scores: null,
        recommendations: null,
        roadmap: null,
        caseStudy: null
    },

    // Initialize application
    init() {
        console.log('🌱 CSA-IRA Tool initialized');
        this.loadStateFromStorage();
        this.setupEventListeners();
        this.showScreen(0);
    },

    // Event listeners
    setupEventListeners() {
        // Profile form submission
        const profileForm = document.getElementById('profile-form');
        if (profileForm) {
            profileForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitProfile();
            });
        }
    },

    // Navigation between screens
    goToScreen(screenNumber) {
        this.showScreen(screenNumber);
        this.state.currentScreen = screenNumber;
        this.saveStateToStorage();
        window.scrollTo(0, 0);
    },

    showScreen(screenNumber) {
        // Hide all screens
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });

        // Show target screen
        const targetScreen = document.getElementById(`screen-${screenNumber}`);
        if (targetScreen) {
            targetScreen.classList.add('active');
        }

        // Initialize screen-specific content
        if (screenNumber === 2) {
            this.initAssessment();
        } else if (screenNumber === 3) {
            this.displayResults();
        } else if (screenNumber === 4) {
            this.displayRoadmap();
        } else if (screenNumber === 5) {
            this.displayActionPlan();
        } else if (screenNumber === 6) {
            this.displayCaseStudy();
        } else if (screenNumber === 7) {
            this.displayExport();
        }
    },

    // Profile submission
    submitProfile() {
        const form = document.getElementById('profile-form');
        const formData = new FormData(form);

        this.state.projectProfile = {
            activityType: formData.get('activity-type'),
            farmSize: formData.get('farm-size'),
            numYouth: parseInt(formData.get('num-youth')),
            numWomen: parseInt(formData.get('num-women')),
            location: formData.get('location')
        };

        this.saveStateToStorage();
        this.goToScreen(2);
    },

    // Assessment functions
    initAssessment() {
        this.state.currentPrinciple = 0;
        this.displayPrinciple(0);
    },

    displayPrinciple(index) {
        const principle = CSA_IRA_QUESTIONS.principles[index];
        if (!principle) return;

        const container = document.getElementById('assessment-container');
        const currentPrincipleSpan = document.getElementById('current-principle');
        const progressBar = document.getElementById('assessment-progress');

        currentPrincipleSpan.textContent = index + 1;
        progressBar.style.width = `${(index / 10) * 100}%`;

        let html = `
            <div class="principle-card fade-in">
                <div class="principle-header">
                    <div class="principle-icon" style="background: linear-gradient(135deg, ${principle.color}, hsl(${principle.color.match(/\d+/)[0]}, 71%, 35%));">
                        ${principle.icon}
                    </div>
                    <div class="principle-info">
                        <div class="principle-title">${principle.title}</div>
                        <div class="principle-number">${principle.number} / 10</div>
                    </div>
                </div>
        `;

        principle.questions.forEach((question, qIndex) => {
            html += `
                <div class="question-item">
                    <div class="question-text">${question.text}</div>
                    <div class="answer-options">
            `;

            question.answers.forEach((answer) => {
                const inputId = `${question.id}-${answer.value}`;
                const isChecked = this.state.assessmentResponses[`p${principle.id}`]?.[qIndex] === answer.value;

                html += `
                    <label class="answer-option">
                        <input type="radio" 
                               name="${question.id}" 
                               value="${answer.value}"
                               id="${inputId}"
                               data-principle="${principle.id}"
                               data-question="${qIndex}"
                               ${isChecked ? 'checked' : ''}
                               onchange="app.recordAnswer(${principle.id}, ${qIndex}, ${answer.value})">
                        <div class="answer-label">
                            <span class="answer-icon">${answer.icon}</span>
                            <span class="answer-text">${answer.text}</span>
                        </div>
                    </label>
                `;
            });

            html += `
                    </div>
                </div>
            `;
        });

        html += `</div>`;
        container.innerHTML = html;

        // Update navigation buttons
        this.updateAssessmentNavigation();
    },

    recordAnswer(principleId, questionIndex, value) {
        const principleKey = `p${principleId}`;

        if (!this.state.assessmentResponses[principleKey]) {
            this.state.assessmentResponses[principleKey] = [];
        }

        this.state.assessmentResponses[principleKey][questionIndex] = value;
        this.saveStateToStorage();
        this.updateAssessmentNavigation();
    },

    updateAssessmentNavigation() {
        const principle = CSA_IRA_QUESTIONS.principles[this.state.currentPrinciple];
        const prevBtn = document.getElementById('prev-principle');
        const nextBtn = document.getElementById('next-principle');

        // Show/hide previous button
        prevBtn.style.display = this.state.currentPrinciple > 0 ? 'block' : 'none';

        // Check if all questions answered
        const principleKey = `p${principle.id}`;
        const answers = this.state.assessmentResponses[principleKey];
        const allAnswered = answers && answers.length === principle.questions.length;

        nextBtn.disabled = !allAnswered;

        // Change text on last principle
        if (this.state.currentPrinciple === 9) {
            nextBtn.textContent = 'Voir mes résultats →';
        } else {
            nextBtn.textContent = 'Suivant →';
        }
    },

    nextPrinciple() {
        if (this.state.currentPrinciple < 9) {
            this.state.currentPrinciple++;
            this.displayPrinciple(this.state.currentPrinciple);
        } else {
            // Assessment complete, calculate scores
            this.calculateScores();
            this.goToScreen(3);
        }
    },

    previousPrinciple() {
        if (this.state.currentPrinciple > 0) {
            this.state.currentPrinciple--;
            this.displayPrinciple(this.state.currentPrinciple);
        }
    },

    // Calculate all scores
    calculateScores() {
        this.state.scores = ScoringEngine.calculateAllScores(this.state.assessmentResponses);
        this.state.recommendations = RecommendationEngine.generateRecommendations(
            this.state.scores,
            this.state.projectProfile
        );
        this.state.roadmap = RoadmapGenerator.generateRoadmap(this.state.scores);
        this.state.caseStudy = getRelevantCaseStudy(
            this.state.projectProfile.activityType,
            this.state.scores.weakPrinciples
        );

        this.saveStateToStorage();
    },

    // Display results screen
    displayResults() {
        if (!this.state.scores) return;

        const { globalScore, profile, principleScores } = this.state.scores;

        // Update score circle
        const scoreValue = document.getElementById('global-score');
        const scoreCircle = document.getElementById('score-circle');
        const profileBadge = document.getElementById('profile-badge');
        const profileMessage = document.getElementById('profile-message');

        // Animate score
        scoreValue.textContent = globalScore;

        // Animate circle (circumference = 2 * π * r = 2 * 3.14159 * 85 ≈ 534)
        const circumference = 534;
        const offset = circumference - (globalScore / 100) * circumference;
        scoreCircle.style.strokeDashoffset = offset;
        scoreCircle.style.stroke = ScoringEngine.getScoreColor(globalScore, true);

        // Profile badge
        profileBadge.innerHTML = `
            <span class="profile-badge" style="background: ${profile.color}; color: white;">
                ${profile.icon} ${profile.name}
            </span>
        `;

        // Profile message
        profileMessage.innerHTML = `<p>${profile.message}</p>`;

        // Principles breakdown
        const principlesContainer = document.getElementById('principles-scores');
        let html = '';

        principleScores.forEach(ps => {
            const principle = CSA_IRA_QUESTIONS.principles[ps.id - 1];
            const scorePercent = Math.round(ps.score * 100);
            const color = ScoringEngine.getScoreColor(ps.score, false);

            html += `
                <div class="principle-score-item">
                    <div class="principle-score-icon">${principle.icon}</div>
                    <div class="principle-score-info">
                        <div class="principle-score-name">${principle.title}</div>
                        <div class="principle-score-bar">
                            <div class="principle-score-fill" 
                                 style="width: ${scorePercent}%; background: ${color};"></div>
                        </div>
                    </div>
                    <div class="principle-score-value">${scorePercent}%</div>
                </div>
            `;
        });

        principlesContainer.innerHTML = html;
    },

    // Display roadmap
    displayRoadmap() {
        if (!this.state.roadmap) return;

        const timeline = this.state.roadmap.timeline;
        const container = document.getElementById('roadmap-timeline');
        const objectiveContainer = document.getElementById('roadmap-objective');

        let html = '';
        timeline.forEach(phase => {
            const activeClass = phase.isActive ? 'active' : '';
            html += `
                <div class="timeline-item ${activeClass}">
                    <div class="timeline-marker"></div>
                    <div class="timeline-content">
                        <div class="timeline-phase">${phase.icon} Phase ${phase.id}</div>
                        <div class="timeline-title">${phase.name}</div>
                        <div class="timeline-duration">Score: ${phase.scoreRange} | ${phase.duration}</div>
                        <div class="timeline-description">
                            ${phase.objectives.map(obj => `• ${obj}`).join('<br>')}
                        </div>
                    </div>
                </div>
            `;
        });

        container.innerHTML = html;

        // Objective
        const message = RoadmapGenerator.getObjectiveMessage(
            this.state.scores.profile,
            this.state.roadmap.nextMilestone
        );

        objectiveContainer.innerHTML = `
            <h3>🎯 Ton objectif</h3>
            <p>${message}</p>
        `;
    },

    // Display action plan
    displayActionPlan() {
        if (!this.state.recommendations) return;

        const { quick, structural, strategic } = this.state.recommendations;
        const container = document.getElementById('action-plan-container');

        let html = '';

        // Quick actions
        html += `
            <div class="action-section">
                <div class="action-section-header">
                    <span class="action-section-icon">✅</span>
                    <h3 class="action-section-title">Actions Rapides</h3>
                    <span class="action-section-label">0-3 mois</span>
                </div>
                <div class="action-list">
        `;

        quick.forEach(action => {
            html += this.renderActionCard(action, 'hsl(142, 71%, 45%)');
        });

        html += `</div></div>`;

        // Structural actions
        html += `
            <div class="action-section">
                <div class="action-section-header">
                    <span class="action-section-icon">⚙️</span>
                    <h3 class="action-section-title">Actions Structurantes</h3>
                    <span class="action-section-label">3-12 mois</span>
                </div>
                <div class="action-list">
        `;

        structural.forEach(action => {
            html += this.renderActionCard(action, 'hsl(38, 92%, 50%)');
        });

        html += `</div></div>`;

        // Strategic actions
        html += `
            <div class="action-section">
                <div class="action-section-header">
                    <span class="action-section-icon">🌱</span>
                    <h3 class="action-section-title">Action Stratégique</h3>
                    <span class="action-section-label">12+ mois</span>
                </div>
                <div class="action-list">
        `;

        strategic.forEach(action => {
            html += this.renderActionCard(action, 'hsl(207, 90%, 54%)');
        });

        html += `</div></div>`;

        container.innerHTML = html;
    },

    renderActionCard(action, color) {
        return `
            <div class="action-card" style="border-left-color: ${color};">
                <div class="action-title">${action.icon} ${action.title}</div>
                <div class="action-description">${action.description}</div>
                <div class="action-meta">
                    <span class="action-tag">📊 ${action.impact}</span>
                    <span class="action-tag">🎯 ${action.principleName}</span>
                </div>
            </div>
        `;
    },

    // Display case study
    displayCaseStudy() {
        if (!this.state.caseStudy) return;

        const cs = this.state.caseStudy;
        const container = document.getElementById('case-study-container');

        const html = `
            <div class="case-study-card">
                <img src="${cs.imageUrl}" alt="${cs.title}" class="case-study-image" 
                     onerror="this.style.display='none'">
                <div class="case-study-content">
                    <div class="case-study-label">${cs.label}</div>
                    <h3 class="case-study-title">${cs.title}</h3>
                    <p>${cs.description}</p>
                    
                    <div class="case-study-section">
                        <h4>Ce qu'ils ont fait</h4>
                        <ul>
                            ${cs.whatTheyDid.map(item => `<li>${item}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="case-study-section">
                        <h4>Ce que tu peux faire à ton niveau</h4>
                        <ul>
                            ${cs.whatYouCanDo.map(item => `<li>${item}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="case-study-section">
                        <h4>Impact potentiel</h4>
                        <p><strong>${cs.impact.score_increase}</strong></p>
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = html;
    },

    // Display export screen
    displayExport() {
        if (!this.state.scores) return;

        document.getElementById('export-score').textContent = `${this.state.scores.globalScore}%`;
        document.getElementById('export-profile').textContent = this.state.scores.profile.name;
        document.getElementById('export-weak-count').textContent = this.state.scores.weakPrinciples.length;
    },

    // Export PDF
    exportPDF() {
        const data = {
            profile: this.state.projectProfile,
            scores: this.state.scores,
            recommendations: this.state.recommendations,
            roadmap: this.state.roadmap
        };

        ExportPDF.generateReport(data);
    },

    // Save progress
    saveProgress() {
        this.saveStateToStorage();
        alert('✅ Ton diagnostic a été sauvegardé ! Tu peux le retrouver en revenant sur cette page.');
    },

    // Restart assessment
    restartAssessment() {
        if (confirm('Es-tu sûr de vouloir recommencer ? Toutes tes réponses seront effacées.')) {
            this.state = {
                currentScreen: 0,
                currentPrinciple: 0,
                projectProfile: {},
                assessmentResponses: {},
                scores: null,
                recommendations: null,
                roadmap: null,
                caseStudy: null
            };
            this.saveStateToStorage();
            this.goToScreen(0);
        }
    },

    // LocalStorage management
    saveStateToStorage() {
        try {
            localStorage.setItem('csa-ira-state', JSON.stringify(this.state));
        } catch (e) {
            console.warn('Could not save to localStorage:', e);
        }
    },

    loadStateFromStorage() {
        try {
            const saved = localStorage.getItem('csa-ira-state');
            if (saved) {
                this.state = JSON.parse(saved);
            }
        } catch (e) {
            console.warn('Could not load from localStorage:', e);
        }
    }
};

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => app.init());
} else {
    app.init();
}
