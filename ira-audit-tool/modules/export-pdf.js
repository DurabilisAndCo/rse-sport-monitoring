// Export PDF Module
// Generates PDF reports using jsPDF

const ExportPDF = {

    // Generate and download PDF report
    // @param projectData: complete project data including profile, scores, recommendations
    generateReport(projectData) {
        // Note: This requires jsPDF library to be loaded
        // For now, we'll create a placeholder that shows what the PDF would contain

        console.log('PDF Export - Project Data:', projectData);

        // Check if jsPDF is available
        if (typeof window.jspdf === 'undefined') {
            console.warn('jsPDF library not loaded. PDF export unavailable.');
            this.downloadTextReport(projectData);
            return;
        }

        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        // PDF Content
        this.addHeader(doc, projectData);
        this.addScoreSummary(doc, projectData);
        this.addPrinciplesBreakdown(doc, projectData);
        this.addRecommendations(doc, projectData);
        this.addRoadmap(doc, projectData);
        this.addFooter(doc);

        // Download
        const filename = `diagnostic-ira-${Date.now()}.pdf`;
        doc.save(filename);
    },

    // Add header to PDF
    addHeader(doc, data) {
        doc.setFontSize(20);
        doc.setTextColor(40, 120, 80);
        doc.text('Diagnostic CSA-IRA', 20, 20);

        doc.setFontSize(12);
        doc.setTextColor(100);
        doc.text(`Type d'activité: ${data.profile.activityType}`, 20, 30);
        doc.text(`Date: ${new Date().toLocaleDateString('fr-FR')}`, 20, 37);
    },

    // Add score summary
    addScoreSummary(doc, data) {
        doc.setFontSize(16);
        doc.setTextColor(40);
        doc.text('Score Global', 20, 50);

        doc.setFontSize(40);
        doc.setTextColor(40, 120, 80);
        doc.text(`${data.scores.globalScore}%`, 20, 65);

        doc.setFontSize(12);
        doc.setTextColor(100);
        doc.text(data.scores.profile.name, 20, 75);
    },

    // Add principles breakdown
    addPrinciplesBreakdown(doc, data) {
        doc.setFontSize(14);
        doc.setTextColor(40);
        doc.text('Scores par Principe', 20, 90);

        let yPos = 100;
        data.scores.principleScores.forEach((p, index) => {
            const principle = CSA_IRA_QUESTIONS.principles[index];
            const score = Math.round(p.score * 100);

            doc.setFontSize(10);
            doc.setTextColor(60);
            doc.text(`${principle.number}: ${principle.title}`, 20, yPos);
            doc.text(`${score}%`, 180, yPos);

            yPos += 7;
        });
    },

    // Add recommendations
    addRecommendations(doc, data) {
        doc.addPage();
        doc.setFontSize(16);
        doc.setTextColor(40);
        doc.text('Plan d\'Action Prioritaire', 20, 20);

        let yPos = 35;

        // Quick actions
        doc.setFontSize(14);
        doc.text('Actions Rapides (0-3 mois)', 20, yPos);
        yPos += 10;

        data.recommendations.quick.forEach((action, index) => {
            doc.setFontSize(10);
            doc.text(`${index + 1}. ${action.title}`, 25, yPos);
            yPos += 7;
        });

        yPos += 10;

        // Structural actions
        doc.setFontSize(14);
        doc.text('Actions Structurantes (3-12 mois)', 20, yPos);
        yPos += 10;

        data.recommendations.structural.forEach((action, index) => {
            doc.setFontSize(10);
            doc.text(`${index + 1}. ${action.title}`, 25, yPos);
            yPos += 7;
        });
    },

    // Add roadmap
    addRoadmap(doc, data) {
        let yPos = 180;

        doc.setFontSize(14);
        doc.setTextColor(40);
        doc.text('Feuille de Route', 20, yPos);
        yPos += 15;

        doc.setFontSize(10);
        doc.setTextColor(100);
        doc.text(`Objectif: ${data.roadmap.nextMilestone.label}`, 20, yPos);
        yPos += 7;
        doc.text(`Durée estimée: ${data.roadmap.estimatedDuration.message}`, 20, yPos);
    },

    // Add footer
    addFooter(doc) {
        const pageCount = doc.internal.getNumberOfPages();

        for (let i = 1; i <= pageCount; i++) {
            doc.setPage(i);
            doc.setFontSize(8);
            doc.setTextColor(150);
            doc.text(
                'Auto-Audit CSA-IRA | Outil d\'évaluation pour l\'investissement agricole responsable',
                20,
                285
            );
            doc.text(`Page ${i} / ${pageCount}`, 180, 285);
        }
    },

    // Fallback: Download as text file if jsPDF is not available
    downloadTextReport(data) {
        let content = '=== DIAGNOSTIC CSA-IRA ===\n\n';
        content += `Date: ${new Date().toLocaleDateString('fr-FR')}\n`;
        content += `Type d'activité: ${data.profile.activityType}\n\n`;
        content += `SCORE GLOBAL: ${data.scores.globalScore}%\n`;
        content += `Profil: ${data.scores.profile.name}\n\n`;
        content += `=== SCORES PAR PRINCIPE ===\n`;

        data.scores.principleScores.forEach((p, index) => {
            const principle = CSA_IRA_QUESTIONS.principles[index];
            const score = Math.round(p.score * 100);
            content += `${principle.number}: ${score}% - ${principle.title}\n`;
        });

        content += `\n=== PLAN D'ACTION ===\n\n`;
        content += `Actions Rapides (0-3 mois):\n`;
        data.recommendations.quick.forEach((action, i) => {
            content += `${i + 1}. ${action.title}\n`;
        });

        content += `\nActions Structurantes (3-12 mois):\n`;
        data.recommendations.structural.forEach((action, i) => {
            content += `${i + 1}. ${action.title}\n`;
        });

        content += `\n=== FEUILLE DE ROUTE ===\n`;
        content += `${data.roadmap.nextMilestone.label}\n`;
        content += `Durée estimée: ${data.roadmap.estimatedDuration.message}\n`;

        // Create download
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `diagnostic-ira-${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
};
