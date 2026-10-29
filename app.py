import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote_plus
import html
from pathlib import Path

st.set_page_config(page_title="MediBill | Pharmacy Billing", layout="wide")

NAVY, BLUE, TEAL = "#17324D", "#2563EB", "#0F766E"
BORDER, INK, MUTED = "#D7DEE7", "#20262E", "#64748B"

# IMAGE PATH FIX:
# Your GitHub screenshot shows the image files beside app.py in the repository root.
# This function supports BOTH layouts:
#   1) app.py and image files in the same folder (your current GitHub layout)
#   2) app.py beside an assets/ folder containing the images
APP_DIR = Path(__file__).resolve().parent
ASSET_DIR = APP_DIR / "assets"

def asset_path(filename):
    """Find an image whether it is beside app.py or inside assets/."""
    if not filename:
        return None

    # Check the repository root first because your uploaded images are there.
    candidates = [APP_DIR / filename, ASSET_DIR / filename]

    for path in candidates:
        if path.is_file():
            return str(path)

    return None

# Product image mapping. Products without a dedicated image use a category image.
PRODUCT_IMAGES = {
    "Digital Thermometer": "digital_thermometer.png",
    "Pulse Oximeter": "pulse_oximeter.png",
    "Limcee": "vitamin_c.png",
    "Celin 500": "vitamin_c.png",
    "Electral": "ors_packet.png",
    "ORS Powder": "ors_packet.png",
    "Digene": "antacid_gaviscon.png",
    "Gelusil": "antacid_gaviscon.png",
    "Band-Aid": "first_aid_bandage.png",
    "Hansaplast": "first_aid_bandage.png",
    "Vaseline Petroleum Jelly": "petroleum_jelly.png",
}
CATEGORY_IMAGES = {
    "Pain relief": "medicine_blister_packs.png",
    "Allergy care": "medicine_blister_packs.png",
    "Cold care": "medicine_blister_packs.png",
    "Throat care": "medicine_capsules.png",
    "Cough care": "medicine_capsules.png",
    "Digestive care": "antacid_gaviscon.png",
    "Hydration": "ors_packet.png",
    "Vitamins": "vitamin_c.png",
    "First aid": "first_aid_bandage.png",
    "Devices": "digital_thermometer.png",
    "Personal care": "petroleum_jelly.png",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {{font-family:Inter,sans-serif;}}
.stApp {{background:#F4F6F9;color:{INK};}}
[data-testid="stSidebar"] {{background:#EEF2F6;border-right:1px solid {BORDER};}}
.hero {{background:linear-gradient(115deg,{NAVY},#244C72 65%,{TEAL});padding:1.3rem 1.5rem;border-radius:15px;color:white;margin-bottom:1rem;}}
.hero h1 {{color:white;margin:0;font-size:2.1rem;}}
.hero p {{color:#E2E8F0;margin:.25rem 0 0 0;}}
div[data-testid="stMetric"] {{background:white;border:1px solid {BORDER};padding:.75rem 1rem;border-radius:10px;}}
div.stButton>button,div.stDownloadButton>button {{border-radius:8px;font-weight:600;}}
.paper-bill {{background:#fffdf2;color:#292820;border:1px solid #c9c4aa;padding:18px;font-family:'Courier New',monospace;box-shadow:0 3px 12px #00000012;}}
.paper-title {{text-align:center;font-weight:bold;font-size:19px;letter-spacing:2px;}}
.paper-subtitle {{text-align:center;font-size:10px;margin:3px 0;}}
.paper-line {{border-top:1px dashed #77745f;margin:9px 0;}}
.paper-meta {{display:flex;justify-content:space-between;gap:8px;font-size:10px;}}
.paper-bill table {{width:100%;border-collapse:collapse;font-family:'Courier New',monospace;font-size:10px;margin-top:8px;}}
.paper-bill th {{border-top:1px solid #6e6b5c;border-bottom:1px solid #6e6b5c;text-align:left;padding:5px 2px;}}
.paper-bill td {{padding:5px 2px;vertical-align:top;border-bottom:1px dotted #c9c4aa;}}
.paper-bill .num {{text-align:right;white-space:nowrap;}}
.paper-total {{text-align:right;font-weight:bold;font-size:14px;margin-top:8px;}}
</style>
""", unsafe_allow_html=True)

# Optional homepage banner image. If the image is absent, the app still works normally.
banner = asset_path("pharmacy_interior.png")
if banner:
    st.image(banner, use_container_width=True)
st.markdown(
    f'<div class="hero"><h1>MediBill</h1><p>Pharmacy catalogue, live billing, basket comparison and a classic paper-style receipt.</p></div>',
    unsafe_allow_html=True,
)

# Educational catalogue with 56 products across multiple manufacturers.
