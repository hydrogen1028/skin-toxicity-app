import streamlit as st
import datetime
from fpdf import FPDF

# ------------------------
# Skin toxicity guidance data
# ------------------------
def get_skin_toxicity_guidance(treatment_type):
    guidance = {
        "Chemotherapy": {
            "Proactive": [
                "Gentle cleanser (pH ~5)",
                "Emollients with niacinamide, ceramides, shea butter",
                "Broad-spectrum sunscreen (SPF ≥ 50)",
                "Scalp cooling for alopecia",
                "Urea cream (10%) for hand-foot prevention"
            ],
            "Reactive": [
                "Urea 3–10% creams for xerosis",
                "TCS/TCI for pruritus and rash",
                "Oral antihistamines",
                "Topical steroids or NSAIDs for photosensitivity",
                "Oral dexamethasone for HFS",
                "Minoxidil or microblading for alopecia"
            ],
            "AEs": ["Xerosis", "Pruritus", "Photosensitivity", "Alopecia", "HFS"]
        },
        "Targeted Therapy": {
            "Proactive": [
                "Gentle cleanser (pH ~5)",
                "Emollients supporting microbiome (niacinamide, ceramides)",
                "SPF ≥ 50 sunscreen, UV protective clothing",
                "Oral doxycycline/minocycline for EGFR rash",
                "Urea 10% for HFS prevention"
            ],
            "Reactive": [
                "Topical and systemic steroids for rash/acneiform rash",
                "Barrier repair creams for folliculitis",
                "Urea 10–40% for hyperkeratotic HFS",
                "Painkillers, lidocaine patches for HFS pain",
                "Minoxidil or PRP for alopecia"
            ],
            "AEs": ["Acneiform rash", "Folliculitis", "Photosensitivity", "Alopecia", "Hyperkeratotic HFS"]
        },
        "Radiation Therapy": {
            "Proactive": [
                "pH-balanced cleanser",
                "Daily moisturizer (not within 2hr of session)",
                "Broad-spectrum sunscreen",
                "Aloe vera from day 1"
            ],
            "Reactive": [
                "Zinc oxide or silver sulfadiazine for dermatitis",
                "Mid-potency topical steroids (e.g., betamethasone)",
                "Sterile dressings or hydrogel pads",
                "Monitor for infection and use antibiotics if needed",
                "Pentoxifylline + vitamin E for chronic fibrosis"
            ],
            "AEs": ["Acute radiation dermatitis", "Chronic dermatitis", "Photosensitivity"]
        },
        "Immunotherapy": {
            "Proactive": [
                "Gentle cleanser",
                "Moisturizers with niacinamide or ceramides",
                "Broad-spectrum sunscreen"
            ],
            "Reactive": [
                "Topical steroids and antihistamines for rash or xerosis",
                "Oral corticosteroids for Grade ≥ 3 reactions",
                "Supportive treatments for pigmentation changes"
            ],
            "AEs": ["Xerosis", "Rash", "Pigmentation changes"]
        }
    }
    return guidance.get(treatment_type)

# ------------------------
# PDF Export
# ------------------------
def generate_pdf(treatment_type, proactive, reactive, aes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Skin Toxicity Guide for {treatment_type}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Generated on {datetime.date.today()}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="Likely Adverse Events:", ln=True)
    pdf.set_font("Arial", size=12)
    for ae in aes:
        pdf.cell(200, 10, txt=f"- {ae}", ln=True)

    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="\nProactive Measures:", ln=True)
    pdf.set_font("Arial", size=12)
    for item in proactive:
        pdf.cell(200, 10, txt=f"- {item}", ln=True)

    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="\nReactive Measures:", ln=True)
    pdf.set_font("Arial", size=12)
    for item in reactive:
        pdf.cell(200, 10, txt=f"- {item}", ln=True)

    path = f"skin_toxicity_{treatment_type.lower().replace(' ', '_')}.pdf"
    pdf.output(path)
    return path

# ------------------------
# Streamlit UI
# ------------------------
st.set_page_config(page_title="Skin Toxicity Guide", layout="centered")
st.title("🎯 Skin Toxicity Management for Cancer Treatment")
st.write("Select a treatment type below to view common skin-related AEs and their management.")

# Sidebar explanation
with st.sidebar:
    st.header("ℹ️ About")
    st.write("This tool provides evidence-based skin toxicity management strategies for cancer treatments. Based on international guidelines including MASCC, ESMO, and AFSOS.")
    st.write("Created: 2025-07")
    st.markdown("---")
    st.write("Contact: clinicalteam@example.com")

# Dropdown
treatment = st.selectbox("Select Cancer Treatment Type:", ["Chemotherapy", "Targeted Therapy", "Radiation Therapy", "Immunotherapy"])

data = get_skin_toxicity_guidance(treatment)
if data:
    st.subheader("🔬 Likely Skin Adverse Events")
    for ae in data["AEs"]:
        st.markdown(f"- {ae}")

    st.subheader("✅ Proactive Measures")
    for item in data["Proactive"]:
        st.markdown(f"- {item}")

    st.subheader("🩹 Reactive Measures")
    for item in data["Reactive"]:
        st.markdown(f"- {item}")

    # Export
    if st.button("📥 Download as PDF"):
        path = generate_pdf(treatment, data["Proactive"], data["Reactive"], data["AEs"])
        with open(path, "rb") as file:
            st.download_button(label="Download PDF", data=file, file_name=path, mime="application/pdf")
