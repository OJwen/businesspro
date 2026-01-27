from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Dict
from ..database import get_db
from ..models import VoiceLog
from ..schemas import VoiceLogRead
import re
from datetime import datetime
import markdown

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

class ProposalGenerator:
    def generate(self, transcript: str, voice_id: str) -> str:
        transcript_lower = transcript.lower()
        budget = self._extract_budget(transcript)
        timeline = self._extract_timeline(transcript)
        category = self._identify_category(transcript_lower)
        template = self._get_template(category)
        
        proposal = template.format(
            voice_id=voice_id,
            budget=budget,
            timeline=timeline,
            date=datetime.now().strftime("%B %d, %Y")
        )
        return proposal

    def _extract_budget(self, text: str) -> str:
        match = re.search(r'\$(\d+(?:,\d+)*(?:k|K|m|M)?)', text)
        if match: return match.group(0)
        return "To be determined based on final scope discovery"

    def _extract_timeline(self, text: str) -> str:
        match = re.search(r'(\d+\s+(?:weeks?|months?))', text, re.IGNORECASE)
        if match: return match.group(1)
        if "q1" in text.lower(): return "Q1 Delivery"
        if "q2" in text.lower(): return "Q2 Delivery"
        if "q3" in text.lower(): return "Q3 Delivery"
        if "q4" in text.lower(): return "Q4 Delivery"
        return "4-8 weeks (Standard estimation)"

    def _identify_category(self, text: str) -> str:
        if any(w in text for w in ['ai', 'chatbot', 'gpt', 'llm', 'intelligence', 'rag']): return 'AI'
        if any(w in text for w in ['app', 'mobile', 'ios', 'android']): return 'MOBILE'
        if any(w in text for w in ['crm', 'erp', 'enterprise', 'system']): return 'ENTERPRISE'
        if any(w in text for w in ['web', 'website', 'scraping']): return 'WEB'
        return 'GENERAL'

    def _get_template(self, category: str) -> str:
        # (Same templates as before, truncated for brevity in this replace, but full content will be written)
        # I'll include the full content to be safe and ensure the file is complete.
        templates_map = {
            'AI': """
# AI & Automation Strategy Proposal

## Executive Summary
We have analyzed your requirement for an intelligent automation solution. Leveraging state-of-the-art Large Language Models (LLMs) and Vector Databases, we propose a custom AI implementation that ensures accuracy, scalability, and measurable ROI.

## Proposed Solution: "IntelliAgent" Architecture
1. **Data Ingestion**
   - Seamless connection to your existing knowledge base.
   - Real-time embedding generation for semantic search.
2. **Core AI Engine**
   - Fine-tuned model layer for domain-specific accuracy.
   - Guardrails to ensure safety and compliance.
3. **User Interface**
   - Responsive web/mobile chat interface.
   - Admin dashboard for analytics and feedback loops.

## Investment Overview
- **Estimated Budget:** {budget}
- **Project Timeline:** {timeline}
- **Maintenance:** Monthly recurring updates and monitoring.

## Why Us?
We don't just build chatbots; we build business agents that drive efficiency. Let's automate the future, together.
""",
            'MOBILE': """
# Mobile Application Development Proposal

## Executive Summary
In today's mobile-first world, your application needs to be more than just functional—it needs to be engaging. We propose a high-performance, cross-platform mobile application (iOS & Android) designed with user retention at its core.

## Technical Approach
1. **UX/UI Design Phase**
   - User journey mapping and high-fidelity prototypes.
   - Focus on intuitive navigation and "gamified" elements (if applicable).
2. **Development (React Native / Flutter)**
   - Single codebase for dual-platform maintenance.
   - Native module integration for maximum performance.
3. **Backend & Cloud**
   - Scalable serverless architecture.
   - Secure API endpoints and real-time database sync.

## Project Scope
- **Target Budget:** {budget}
- **Development Timeline:** {timeline}

## Next Steps
We are ready to move to the wireframing stage immediately upon approval.
""",
            'ENTERPRISE': """
# Enterprise System Modernization Proposal

## Executive Summary
Legacy systems are the bottleneck of growth. We understand your need for a robust, integrated system overhaul. Our proposal outlines a secure, phased migration strategy to modernize your infrastructure without business disruption.

## Strategic Roadmap
1. **Audit & Analysis**
   - Comprehensive review of current data flows and pain points.
2. **System Architecture Design**
   - Microservices-based architecture for flexibility.
   - API-first approach for seamless 3rd-party integrations (CRM, ERP, Marketing).
3. **Implementation & Migration**
   - Iterative development (Sprints).
   - Data cleaning and safe migration protocols.

## Commercial Terms
- **Investment Estimate:** {budget}
- **Execution Timeline:** {timeline}

## Verification & Compliance
All deliverables will adhere to industry standards (SOC2 / ISO where applicable) and undergo rigorous penetration testing.
""",
            'WEB': """
# Web Development & Data Solutions Proposal

## Executive Summary
We propose a scalable web solution tailored to your specific data needs. Whether it is a customer-facing portal or a high-throughput data scraping dashboard, our stack ensures speed, security, and reliability.

## Solution Details
1. **Frontend Experience**
   - Modern framework (React/Next.js) for SEO and performance.
   - Responsive design for all devices.
2. **Data Pipeline & Backend**
   - Robust Python/Node.js backend.
   - Automated data extraction and processing pipelines.
3. **Analytics Dashboard**
   - Real-time visualization of key metrics.
   - Export capabilities (CSV, PDF).

## Project Plan
- **Budget Allocation:** {budget}
- **Delivery Timeline:** {timeline}

## Conclusion
We are confident this solution will provide the visibility and efficiency your team requires.
""",
            'GENERAL': """
# Digital Transformation Proposal

## Executive Summary
We are pleased to submit this proposal to support your digital initiatives. Our team specializes in translating complex business requirements into elegant technical solutions.

## Proposed Strategy
1. **Discovery**: Aligning technology with your business goals.
2. **Development**: Custom software development using modern best practices.
3. **Support**: Long-term partnership and technical support.

## Project Estimates
- **Budget:** {budget}
- **Timeline:** {timeline}

## Why Choose Us?
We bring expertise, transparency, and a results-driven approach to every project.
"""
        }
        return templates_map.get(category, templates_map['GENERAL'])


generator = ProposalGenerator()

@router.get("/", response_model=List[VoiceLogRead])
def read_voice_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = db.query(VoiceLog).order_by(VoiceLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/{voice_log_id}/proposal")
def generate_proposal(voice_log_id: int, db: Session = Depends(get_db)):
    log = db.query(VoiceLog).filter(VoiceLog.id == voice_log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Voice log not found")
    
    proposal_text = generator.generate(log.transcript, log.elevenlabs_voice_id)
    return {"id": log.id, "voice_id": log.elevenlabs_voice_id, "proposal": proposal_text}

@router.get("/{voice_log_id}/proposal/html", response_class=HTMLResponse)
def view_proposal_html(request: Request, voice_log_id: int, db: Session = Depends(get_db)):
    log = db.query(VoiceLog).filter(VoiceLog.id == voice_log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Voice log not found")
    
    proposal_md = generator.generate(log.transcript, log.elevenlabs_voice_id)
    # Convert MD to HTML
    proposal_html_content = markdown.markdown(proposal_md)
    
    return templates.TemplateResponse("proposal.html", {
        "request": request,
        "voice_id": log.elevenlabs_voice_id,
        "date": datetime.now().strftime("%B %d, %Y"),
        "proposal_html": proposal_html_content
    })
