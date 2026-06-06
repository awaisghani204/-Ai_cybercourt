from fpdf import FPDF

class CourtPDF(FPDF):
    def header(self):
        # Court Header
        self.set_font("helvetica", "B", 20)
        self.cell(0, 10, "THE AI CYBER-COURT", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("helvetica", "I", 12)
        self.cell(0, 10, "Official Court Transcript", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(5)
        
        # Court Stamp
        self.set_text_color(200, 0, 0)
        self.set_font("helvetica", "B", 14)
        self.cell(0, 10, "[ OFFICIAL COURT DOCUMENT - VERIFIED ]", border=1, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_transcript_pdf(crime_description, debate_history, jury_vote, final_verdict):
    pdf = CourtPDF()
    pdf.add_page()
    
    # Body font
    pdf.set_font("helvetica", size=11)
    
    # Crime
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "CASE DETAILS:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=11)
    pdf.multi_cell(0, 8, f"Crime: {crime_description}")
    pdf.ln(5)
    
    # Debate
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "DEBATE TRANSCRIPT:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=11)
    
    for msg in debate_history:
        role = msg['role'].upper()
        text = msg['text']
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 8, f"{role}:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", size=11)
        pdf.multi_cell(0, 8, text)
        pdf.ln(3)
        
    pdf.ln(5)
    
    # Jury Vote
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "JURY VOTE:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=11)
    pdf.cell(0, 8, str(jury_vote), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Verdict
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "FINAL VERDICT:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", size=11)
    pdf.multi_cell(0, 8, final_verdict)
    
    # Output bytes
    return bytes(pdf.output())
