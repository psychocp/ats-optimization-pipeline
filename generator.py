from fpdf import FPDF
import io

class ATSResumePDF(FPDF):
    def header(self):
        pass
    def footer(self):
        pass

def build_ats_friendly_pdf(data: dict) -> io.BytesIO:
    """Generates a mathematically perfect, single-column, highly parsable ATS PDF using FPDF2."""
    pdf = ATSResumePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Use crisp, clear standard standard fonts (Arial/Helvetica)
    pdf.set_text_color(17, 17, 17) # #111111
    
    # 1. NAME Header
    pdf.set_font("Helvetica", "B", 24)
    name = data.get('name', 'John Doe').upper()
    pdf.cell(0, 10, name, ln=True, align="C")
    
    # 2. CONTACT INFO
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(85, 85, 85) # #555555
    contact_str = f"{data.get('email', '')}  |  {data.get('phone', '')}  |  {data.get('location', '')}  |  {data.get('linkedin', '')}"
    pdf.cell(0, 8, contact_str, ln=True, align="C")
    pdf.ln(4)
    
    pdf.set_text_color(17, 17, 17)
    
    # Helper function for Section Headers to ensure 100% linear text reading layout
    def add_section_header(title):
        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 6, title.upper(), ln=True)
        # Structural separating line
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 180, pdf.get_y())
        pdf.ln(3)

    # 3. SUMMARY SECTION
    add_section_header("Professional Summary")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, data.get('summary', ''))
    
    # 4. SKILLS SECTION
    add_section_header("Core Skills")
    pdf.set_font("Helvetica", "B", 11)
    skills_list = ", ".join(data.get('skills', []))
    pdf.multi_cell(0, 6, skills_list)
    
    # 5. EXPERIENCE SECTION
    add_section_header("Professional Experience")
    for exp in data.get("experience", []):
        pdf.set_font("Helvetica", "B", 11)
        # Left side: Title/Company
        title_company = f"{exp.get('role')} - {exp.get('company')}"
        duration = str(exp.get('duration', ''))
        
        # Format inline header with dates on the right
        pdf.cell(130, 6, title_company)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(50, 6, duration, ln=True, align="R")
        
        # Experience Description Text
        pdf.set_font("Helvetica", "", 10.5)
        pdf.set_text_color(68, 68, 68) # #444444
        pdf.multi_cell(0, 5.5, exp.get('description', ''))
        pdf.ln(2)
        pdf.set_text_color(17, 17, 17)
        
    # 6. EDUCATION SECTION
    add_section_header("Education")
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(130, 6, data.get('education_degree', ''))
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(50, 6, str(data.get('education_year', '')), ln=True, align="R")
    pdf.cell(0, 6, data.get('education_school', ''), ln=True)

    # Return as an in-memory Byte Stream for FastAPI
    pdf_output = pdf.output()
    return io.BytesIO(pdf_output)