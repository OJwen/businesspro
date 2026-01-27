from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import re

def generate_pdf(context):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    # Custom styles
    styles.add(ParagraphStyle(name='CoverTitle', parent=styles['Title'], fontSize=40, leading=50, textColor=colors.HexColor("#2c3e50"), spaceAfter=30))
    styles.add(ParagraphStyle(name='CoverSubtitle', parent=styles['Normal'], fontSize=18, textColor=colors.HexColor("#7f8c8d")))
    styles.add(ParagraphStyle(name='HeadingBlue', parent=styles['Heading1'], textColor=colors.HexColor("#2c3e50"), borderPadding=10, borderColor=colors.HexColor("#38bdf8"), borderWidth=0, borderBottomWidth=2))
    
    story = []
    
    # --- Cover Page ---
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("ANTIGRAVITY", styles['Heading2']))
    story.append(Paragraph("BUSINESS PROPOSAL", styles['CoverTitle']))
    story.append(Paragraph("Custom Solutions for Sustainable Success", styles['CoverSubtitle']))
    story.append(Spacer(1, 3*inch))
    
    # Metadata on cover
    data_table = [
        ["PRESENTED FOR:", context.get("voice_id", "Client")],
        ["DATE:", context.get("date", "")]
    ]
    t = Table(data_table, colWidths=[200, 200])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#2c3e50")),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ]))
    story.append(t)
    story.append(PageBreak())
    
    # --- Content ---
    story.append(Paragraph("Proposal Details", styles['HeadingBlue']))
    story.append(Spacer(1, 20))
    
    # Process Markdown text simply (convert to ReportLab Paragraphs)
    raw_text = context.get("proposal_markdown", "")
    
    for line in raw_text.split('\n'):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 10))
            continue
        
        # Format bold text
        line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
        
        if line.startswith('# '):
            story.append(Paragraph(line[2:], styles['HeadingBlue']))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], styles['Heading2']))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], styles['Heading3']))
        elif line.startswith('- '):
            story.append(Paragraph(f"• {line[2:]}", styles['BodyText']))
        else:
            story.append(Paragraph(line, styles['BodyText']))
            
    story.append(PageBreak())
    
    # --- Team Section ---
    story.append(Paragraph("Our Team", styles['HeadingBlue']))
    story.append(Paragraph("Meet the experts dedicated to your success.", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Team Table
    team_data = [
        ["Sebastian Bennet", "Hannah Morales", "Juliana Silva"],
        ["CEO", "Project Manager", "Marketing"]
    ]
    team_table = Table(team_data, colWidths=[150, 150, 150])
    team_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#2c3e50")),
    ]))
    story.append(team_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer
