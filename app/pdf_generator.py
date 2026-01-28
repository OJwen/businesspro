from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, Path
from reportlab.lib.colors import HexColor
import re

# --- Design Constants ---
COLOR_PRIMARY = HexColor("#2c4a87")  # Dark Blue
COLOR_ACCENT = HexColor("#22396b")   # Darker/Saturated Blue for overlays
COLOR_TEXT_WHITE = HexColor("#FFFFFF")
COLOR_TEXT_DARK = HexColor("#333333")
COLOR_LIGHT_BG = HexColor("#F5F7FA")

def draw_cover_background(canvas, doc):
    """
    Draws the geometric blue background for the cover page.
    """
    canvas.saveState()
    w, h = A4
    
    # 1. Full Dark Blue Background
    canvas.setFillColor(COLOR_PRIMARY)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    
    # 2. Geometric Accent (Diagonal overlay)
    # Simulating the angular cut on the top-right/middle
    canvas.setFillColor(COLOR_ACCENT)
    p = canvas.beginPath()
    p.moveTo(w, h)        # Top right
    p.lineTo(w, h * 0.4)  # Right side, down a bit
    p.lineTo(w * 0.3, h)  # Top side, left a bit
    p.close()
    canvas.drawPath(p, fill=1, stroke=0)
    
    # 3. Bottom Left Geometric Accent
    canvas.setFillColor(COLOR_ACCENT)
    p2 = canvas.beginPath()
    p2.moveTo(0, 0)
    p2.lineTo(w * 0.4, 0)
    p2.lineTo(0, h * 0.3)
    p2.close()
    canvas.drawPath(p2, fill=1, stroke=0)
    
    # 4. Logo / Brand Name (Top Left)
    # Placeholder for logo icon
    canvas.setFillColor(COLOR_TEXT_WHITE)
    # Simple icon
    canvas.rect(20*mm, h - 30*mm, 10*mm, 10*mm, fill=1, stroke=0)
    
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(35*mm, h - 26*mm, "ANTIGRAVITY")
    canvas.setFont("Helvetica", 12)
    canvas.drawString(35*mm, h - 31*mm, "AGENCY")
    
    # 5. Date (Top Right)
    canvas.setFont("Helvetica", 10)
    canvas.drawRightString(w - 20*mm, h - 30*mm, doc.doc_date)
    
    # 6. Bottom Text
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(20*mm, 30*mm, "PRESENTED BY")
    canvas.setFont("Helvetica", 10)
    canvas.drawString(20*mm, 25*mm, "ANTIGRAVITY TEAM")
    
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(w/2, 30*mm, "PREPARED FOR")
    canvas.setFont("Helvetica", 10)
    canvas.drawString(w/2, 25*mm, doc.doc_client_name)
    
    canvas.setFont("Helvetica-Bold", 30)
    canvas.drawRightString(w - 20*mm, 25*mm, "2026")

    canvas.restoreState()

def draw_content_background(canvas, doc):
    """
    Draws the background for normal content pages.
    """
    canvas.saveState()
    w, h = A4
    
    # 1. Top Blue Accent
    # A subtle blue geometric shape at the top right
    canvas.setFillColor(COLOR_PRIMARY)
    p = canvas.beginPath()
    p.moveTo(w, h)
    p.lineTo(w, h - 40*mm)
    p.lineTo(w - 60*mm, h)
    p.close()
    canvas.drawPath(p, fill=1, stroke=0)
    
    # 2. Bottom Right Page Number Box
    canvas.setFillColor(COLOR_PRIMARY)
    canvas.rect(w - 20*mm, 10*mm, 20*mm, 15*mm, fill=1, stroke=0)
    
    canvas.setFillColor(COLOR_TEXT_WHITE)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawCentredString(w - 10*mm, 15*mm, str(doc.page))
    
    # 3. Footer URL
    canvas.setFillColor(COLOR_TEXT_DARK)
    canvas.setFont("Helvetica", 9)
    canvas.drawString(20*mm, 15*mm, "www.antigravity.com")

    canvas.restoreState()

def generate_pdf(context):
    buffer = BytesIO()
    doc = BaseDocTemplate(buffer, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=20*mm, bottomMargin=30*mm)
    
    # Store metadata on doc for callbacks
    doc.doc_date = context.get("date", "")
    doc.doc_client_name = context.get("client_name", "Valued Client")
    
    # --- Frames ---
    # Cover Frame (Full Page)
    frame_cover = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 100*mm, id='cover', showBoundary=0)
    
    # Content Frame
    frame_content = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='content', showBoundary=0)
    
    # --- Page Templates ---
    template_cover = PageTemplate(id='Cover', frames=[frame_cover], onPage=draw_cover_background)
    template_content = PageTemplate(id='Content', frames=[frame_content], onPage=draw_content_background)
    
    doc.addPageTemplates([template_cover, template_content])
    
    # --- Styles ---
    styles = getSampleStyleSheet()
    
    # Cover Styles
    style_cover_title = ParagraphStyle(
        name='CoverTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=48,
        leading=55,
        textColor=COLOR_TEXT_WHITE,
        spaceAfter=10
    )
    style_cover_subtitle = ParagraphStyle(
        name='CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=COLOR_TEXT_WHITE,
        spaceBefore=10
    )
    
    # Content Styles
    style_heading1 = ParagraphStyle(
        name='CustomH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=COLOR_PRIMARY,
        spaceBefore=20,
        spaceAfter=10,
        textTransform='uppercase'
    )
    style_heading2 = ParagraphStyle(
        name='CustomH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=COLOR_TEXT_DARK,
        spaceBefore=15,
        spaceAfter=8,
        backColor=COLOR_LIGHT_BG,
        borderPadding=5
    )
    style_body = ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=COLOR_TEXT_DARK,
        spaceAfter=10
    )

    story = []
    
    # --- Cover Page Content ---
    story.append(Spacer(1, 40*mm)) # Push down text
    story.append(Paragraph("BUSINESS", style_cover_title))
    story.append(Paragraph("PROPOSAL", style_cover_title))
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph("CUSTOM SOLUTIONS FOR SUSTAINABLE SUCCESS", style_cover_subtitle))
    
    # Force Page Break to get to content
    story.append(PageBreak())
    
    # --- Main Content ---
    # Switch to Content Template automatically happens after PageBreak if not specified, 
    # but let's be explicit if needed. Since we only have 2 templates and Cover is first, 
    # next page defaults to next template or same if not handled. 
    from reportlab.platypus import NextPageTemplate
    story.insert(len(story)-1, NextPageTemplate('Content'))
    
    # --- Process Markdown ---
    raw_text = context.get("proposal_markdown", "")
    
    for line in raw_text.split('\n'):
        line = line.strip()
        if not line:
            story.append(Spacer(1, 5))
            continue
        
        # Format bold text
        line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
        
        if line.startswith('# '):
            # Treat # H1 as major section title
            story.append(Paragraph(line[2:], style_heading1))
            story.append(Spacer(1, 5))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], style_heading2))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], style_heading2)) # Map H3 to H2 style for consistency
        elif line.startswith('- '):
            story.append(Paragraph(f"• {line[2:]}", style_body))
        else:
            story.append(Paragraph(line, style_body))
            
    # --- Add Team / About Us Section (Hardcoded for flair if missing from MD) ---
    story.append(PageBreak())
    story.append(Paragraph("OUR TEAM", style_heading1))
    story.append(Paragraph("Meet the experts dedicated to your success.", style_body))
    story.append(Spacer(1, 10))
    
    # Simple Team Table
    team_data = [
        ["Sebastian Bennet", "Hannah Morales", "Juliana Silva"],
        ["CEO", "Project Manager", "Marketing"]
    ]
    t = Table(team_data, colWidths=[50*mm, 50*mm, 50*mm])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (-1,-1), COLOR_PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('TOPPADDING', (0,0), (-1,-1), 15),
    ]))
    story.append(t)
    
    doc.build(story)
    buffer.seek(0)
    return buffer
