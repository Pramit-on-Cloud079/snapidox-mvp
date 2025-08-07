from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import os

# ✅ Use DejaVuSans instead of broken NotoColorEmoji
font_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'utils', 'fonts'))
pdfmetrics.registerFont(TTFont("CleanFont", os.path.join(font_dir, "DejaVuSans.ttf")))

def generate_detailed_pdf(title, summary, tech_stack, features, architecture, pdf_path):
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()

    # Define or update styles
    styles.add(ParagraphStyle(name='CenteredTitle', fontName='CleanFont', fontSize=20, alignment=TA_CENTER, spaceAfter=24, leading=24, textColor=HexColor('#4F46E5')))
    styles.add(ParagraphStyle(name='SectionHeader', fontName='CleanFont', fontSize=15, spaceAfter=14, leading=18, textColor=HexColor('#111827')))
    styles.add(ParagraphStyle(name='BodyTextCustom', fontName='CleanFont', fontSize=11.5, leading=16, spaceAfter=8))
    styles.add(ParagraphStyle(name='Watermark', fontName='CleanFont', fontSize=10, textColor=HexColor('#6B7280'), alignment=TA_CENTER, spaceBefore=30))

    def parse_to_bullets(raw_text):
        if not raw_text.strip():
            return [Paragraph("❌ No content found.", styles['BodyTextCustom'])]
        bullets = []
        for line in raw_text.strip().split('\n'):
            line = line.strip()
            if line:
                bullets.append(ListItem(Paragraph(line, styles['BodyTextCustom'])))
        return [ListFlowable(bullets, bulletType='bullet', start='•', leftIndent=15, spaceBefore=2, spaceAfter=8)]

    # Clean title if quoted
    clean_title = title.strip('"').strip()

    elements = []
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(clean_title, styles['CenteredTitle']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(summary.strip(), styles['BodyTextCustom']))
    elements.append(Spacer(1, 18))

    sections = [
        ("🛠️ Tech Stack", tech_stack),
        ("🚀 Features", features),
        ("🧠 Architecture", architecture)
    ]

    for title, content in sections:
        elements.append(Paragraph(title, styles['SectionHeader']))
        elements.extend(parse_to_bullets(content))
        elements.append(Spacer(1, 12))

    elements.append(Paragraph("🔗 Generated with Snapidox — https://github.com/pramitcodes/snapidox", styles['Watermark']))

    doc.build(elements)