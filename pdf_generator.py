"""
Professional PDF Report Generator for RSE Sport Monitoring
AFD-style report generation with ReportLab
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

# Durabilis & Co Colors
DURABILIS_BLUE = colors.HexColor('#00A9E0')
DURABILIS_DARK_BLUE = colors.HexColor('#2E3192')
DURABILIS_GREY = colors.HexColor('#58595B')
AFD_RED = colors.HexColor('#E74C3C')
AFD_GREEN = colors.HexColor('#27AE60')
AFD_WARNING = colors.HexColor('#F39C12')

class AFDReportGenerator:
    """Generate professional AFD-style PDF reports"""
    
    def __init__(self, project_data, all_projects=None, recommendations=None):
        self.project = project_data
        self.all_projects = all_projects or []
        self.recommendations = recommendations or []
        self.buffer = BytesIO()
        self.width, self.height = A4
        
    def generate(self):
        """Generate the complete PDF report"""
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Build document elements
        story = []
        
        # PAGE 1 - RECTO
        story.extend(self._build_page_1())
        
        # PAGE 2 - VERSO
        story.append(PageBreak())
        story.extend(self._build_page_2())
        
        # Build PDF
        doc.build(story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
        
        self.buffer.seek(0)
        return self.buffer
    
    def _build_page_1(self):
        """Build Page 1 - Context and Results"""
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=DURABILIS_DARK_BLUE,
            spaceAfter=20,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=DURABILIS_DARK_BLUE,
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        title = Paragraph(f"<b>{self.project.get('name', 'Projet RSE & Sport')}</b>", title_style)
        story.append(title)
        story.append(Spacer(1, 0.5*cm))
        
        # Key Data Block (colored box)
        key_data = self._build_key_data_block()
        story.append(key_data)
        story.append(Spacer(1, 0.8*cm))
        
        # Context Section
        story.append(Paragraph("<b>1. CONTEXTE DU PROJET</b>", heading_style))
        context_text = self.project.get('description', '') or "Description du contexte du projet RSE & Sport."
        story.append(Paragraph(context_text, styles['BodyText']))
        story.append(Spacer(1, 0.5*cm))
        
        # Objectives
        story.append(Paragraph("<b>2. OBJECTIFS</b>", heading_style))
        objectives_text = f"""
        Le projet vise à contribuer aux objectifs de développement durable à travers le sport.
        Bénéficiaires estimés : <b>{self.project.get('beneficiaries', 0):,}</b> personnes.
        Budget alloué : <b>{self.project.get('budget', 0):,.0f} €</b>
        """
        story.append(Paragraph(objectives_text, styles['BodyText']))
        story.append(Spacer(1, 0.5*cm))
        
        # Results section
        story.append(Paragraph("<b>3. PRINCIPAUX RÉSULTATS</b>", heading_style))
        results_table = self._build_results_table()
        story.append(results_table)
        story.append(Spacer(1, 0.5*cm))
        
        # Focus section (red box)
        focus_box = self._build_focus_box()
        story.append(focus_box)
        
        return story
    
    def _build_page_2(self):
        """Build Page 2 - Conclusions and Recommendations"""
        story = []
        styles = getSampleStyleSheet()
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=DURABILIS_DARK_BLUE,
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Conclusions
        story.append(Paragraph("<b>4. CONCLUSIONS DE L'ÉVALUATION</b>", heading_style))
        
        # Comparative table: Positives vs Concerns
        comparison_table = self._build_comparison_table()
        story.append(comparison_table)
        story.append(Spacer(1, 0.8*cm))
        
        # Case study (grey box)
        case_study_box = self._build_case_study_box()
        story.append(case_study_box)
        story.append(Spacer(1, 0.8*cm))
        
        # Recommendations (blue box)
        recommendations_box = self._build_recommendations_box()
        story.append(recommendations_box)
        
        return story
    
    def _build_key_data_block(self):
        """Build colored key data block"""
        data = [
            ['PÉRIMÈTRE', self.project.get('location', 'N/A')],
            ['ZONE D\'INTERVENTION', self.project.get('country', 'N/A')],
            ['ORGANISATION', self.project.get('organization', 'N/A')],
            ['BUDGET', f"{self.project.get('budget', 0):,.0f} €"],
            ['PÉRIODE', f"{self.project.get('start_date', 'N/A')} - {self.project.get('end_date', 'N/A')}"],
            ['ÉVALUATION PAR', 'Durabilis & Co']
        ]
        
        table = Table(data, colWidths=[5*cm, 10*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), DURABILIS_BLUE),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white)
        ]))
        
        return table
    
    def _build_results_table(self):
        """Build results infographic table"""
        sports = ', '.join(self.project.get('sports', [])) if self.project.get('sports') else 'N/A'
        sdgs_count = len(self.project.get('sdgs', []))
        participants = self.project.get('indicator_participants', 0)
        sessions = self.project.get('indicator_sessions', 0)
        
        data = [
            ['📊 INDICATEUR', 'VALEUR'],
            ['Sports pratiqués', sports],
            ['Nombre d\'ODD alignés', str(sdgs_count)],
            ['Participants', f'{participants:,}'],
            ['Sessions organisées', f'{sessions:,}'],
            ['Impact social', self.project.get('impact_social', 'Moyen')],
            ['Impact environnemental', self.project.get('impact_environmental', 'Moyen')]
        ]
        
        table = Table(data, colWidths=[8*cm, 7*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), DURABILIS_DARK_BLUE),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, DURABILIS_GREY)
        ]))
        
        return table
    
    def _build_focus_box(self):
        """Build focus section with red accent"""
        styles = getSampleStyleSheet()
        
        focus_data = [[
            Paragraph("<b>FOCUS - CHIFFRES CLÉS</b>", styles['Heading3']),
        ], [
            Paragraph(f"""
            ✓ <b>{self.project.get('beneficiaries', 0):,}</b> bénéficiaires directs<br/>
            ✓ <b>{len(self.project.get('sports', []))}</b> disciplines sportives<br/>
            ✓ <b>{len(self.project.get('sdgs', []))}</b> ODD adressés<br/>
            ✓ Budget : <b>{self.project.get('budget', 0):,.0f} €</b>
            """, styles['BodyText'])
        ]]
        
        table = Table(focus_data, colWidths=[15*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF5F5')),
            ('BOX', (0, 0), (-1, -1), 2, AFD_RED),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        return table
    
    def _build_comparison_table(self):
        """Build comparison table: positives vs concerns"""
        data = [
            ['✅ POINTS POSITIFS', '⚠️ POINTS DE VIGILANCE'],
            [
                '• Alignement fort avec les ODD\n• Engagement communautaire\n• Diversité des activités',
                '• Suivi des indicateurs à renforcer\n• Pérennité financière\n• Coordination parties prenantes'
            ],
        ]
        
        table = Table(data, colWidths=[7.5*cm, 7.5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), AFD_GREEN),
            ('BACKGROUND', (1, 0), (1, 0), AFD_WARNING),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, DURABILIS_GREY)
        ]))
        
        return table
    
    def _build_case_study_box(self):
        """Build case study section (grey box)"""
        styles = getSampleStyleSheet()
        
        case_data = [[
            Paragraph("<b>ÉTUDE DE CAS</b>", styles['Heading3']),
        ], [
            Paragraph(f"""
            <b>Projet pilote : {self.project.get('name', 'N/A')}</b><br/><br/>
            Ce projet illustre l'impact concret du sport comme vecteur de développement.
            Les {self.project.get('beneficiaries', 0):,} bénéficiaires ont participé à 
            {self.project.get('indicator_sessions', 0)} sessions sportives, contribuant ainsi
            à l'amélioration de leur bien-être et à la cohésion sociale.
            """, styles['BodyText'])
        ]]
        
        table = Table(case_data, colWidths=[15*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F5F5F5')),
            ('BOX', (0, 0), (-1, -1), 1, DURABILIS_GREY),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        return table
    
    def _build_recommendations_box(self):
        """Build recommendations section (blue box)"""
        styles = getSampleStyleSheet()
        
        # Format recommendations
        recs_text = ""
        if self.recommendations:
            for i, rec in enumerate(self.recommendations[:5], 1):
                recs_text += f"{i}. <b>{rec.get('title', '')}</b>: {rec.get('description', '')}<br/>"
        else:
            recs_text = "• Renforcer le suivi et l'évaluation<br/>• Développer les partenariats<br/>• Assurer la pérennité des actions"
        
        rec_data = [[
            Paragraph("<b>PRÉCONISATIONS POUR FUTURS PROGRAMMES</b>", styles['Heading3']),
        ], [
            Paragraph(recs_text, styles['BodyText'])
        ]]
        
        table = Table(rec_data, colWidths=[15*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E8F4F8')),
            ('BOX', (0, 0), (-1, -1), 2, DURABILIS_BLUE),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        return table
    
    def _header_footer(self, canvas, doc):
        """Add header and footer to each page"""
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica-Bold', 10)
        canvas.setFillColor(DURABILIS_DARK_BLUE)
        canvas.drawString(2*cm, self.height - 1.5*cm, "Durabilis & Co")
        canvas.setFont('Helvetica', 8)
        canvas.drawString(2*cm, self.height - 1.8*cm, "Data Monitoring - Projet RSE & Sport")
        
        # Footer
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(DURABILIS_GREY)
        canvas.drawString(2*cm, 1.5*cm, f"© {datetime.now().year} Durabilis & Co - Tous droits réservés")
        canvas.drawRightString(self.width - 2*cm, 1.5*cm, f"Page {doc.page}")
        
        canvas.restoreState()


def generate_pdf_report(project, all_projects=None, recommendations=None):
    """
    Generate a professional PDF report for a project
    
    Args:
        project: Project data dictionary
        all_projects: List of all projects (optional)
        recommendations: List of recommendations (optional)
    
    Returns:
        BytesIO buffer containing the PDF
    """
    generator = AFDReportGenerator(project, all_projects, recommendations)
    return generator.generate()
