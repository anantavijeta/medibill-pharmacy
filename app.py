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
    product_col, receipt_col = st.columns([1.4,1], gap="large")
    with product_col:
        st.subheader("Product catalogue")
        search = st.text_input("Search by brand, ingredient or company", placeholder="e.g., Dolo, Cipla, vitamin")
        categories = ["All categories"] + sorted({p["category"] for p in PRODUCTS.values()})
        category = st.selectbox("Filter category", categories)
        shown = [n for n,p in PRODUCTS.items()
                 if (search.lower() in n.lower() or search.lower() in p["generic"].lower() or search.lower() in p["company"].lower())
                 and (category == "All categories" or p["category"] == category)]
        st.caption(f"{len(shown)} products shown · {len(PRODUCTS)} catalogue entries")
        for start in range(0, len(shown), 2):
            cols = st.columns(2)
            for idx, name in enumerate(shown[start:start+2]):
                item = PRODUCTS[name]
                with cols[idx]:
                    with st.container(border=True):
                        image_file = (
                            PRODUCT_IMAGES.get(name)
                            or CATEGORY_IMAGES.get(item["category"])
                            or "medicine_blister_packs.png"
                        )
                        image_path = asset_path(image_file)

                        if image_path:
                            st.image(image_path, use_container_width=True)
                        else:
                            st.markdown(
                                "<div style='height:120px;display:flex;align-items:center;"
                                "justify-content:center;background:#EEF2F6;border-radius:10px;"
                                "color:#64748B;font-size:14px;'>Product image unavailable</div>",
                                unsafe_allow_html=True,
                            )
                        st.markdown(f"**{name}**")
                        st.caption(item["generic"])
                        st.markdown(f"<span style='color:{TEAL};font-weight:700'>{money(item['price'])}</span>", unsafe_allow_html=True)
                        st.caption(f"{item['company']} · {item['category']}")
                        st.number_input("Quantity", min_value=0, max_value=100, step=1, key="qty_" + name)
    with receipt_col:
        cart = {n:int(st.session_state["qty_"+n]) for n in PRODUCTS if int(st.session_state["qty_"+n]) > 0}
        bill = calculate_bill(cart, discount_rate, delivery_fee, membership, tax_rate)
        st.subheader("Printed-paper style receipt")
        st.caption("Updates when you change products or order settings.")
        st.markdown(receipt_html(cart,bill,discount_choice,delivery_method,st.session_state.invoice_no), unsafe_allow_html=True)
        if cart:
            rows = [{"Product":n,"Company":PRODUCTS[n]["company"],"Description":PRODUCTS[n]["generic"],
                     "Quantity":q,"Unit price":PRODUCTS[n]["price"],"Amount":PRODUCTS[n]["price"]*q}
                    for n,q in cart.items()]
            rows += [
                {"Product":"Subtotal","Company":"","Description":"","Quantity":"","Unit price":"","Amount":bill["subtotal"]},
                {"Product":"Discount","Company":"","Description":discount_choice,"Quantity":"","Unit price":"","Amount":-bill["discount"]},
                {"Product":"Membership benefit","Company":"","Description":"","Quantity":"","Unit price":"","Amount":-bill["membership"]},
                {"Product":"Illustrative tax","Company":"","Description":tax_choice,"Quantity":"","Unit price":"","Amount":bill["tax"]},
                {"Product":"Delivery","Company":"","Description":delivery_method,"Quantity":"","Unit price":"","Amount":bill["delivery"]},
                {"Product":"TOTAL","Company":"","Description":"","Quantity":"","Unit price":"","Amount":bill["total"]},
            ]
            st.download_button("Download itemised receipt (CSV)", pd.DataFrame(rows).to_csv(index=False).encode("utf-8"),
                file_name=f"medibill_{st.session_state.invoice_no}.csv", mime="text/csv", use_container_width=True)
        st.button("Clear cart", use_container_width=True, on_click=clear_cart)

with bundles_tab:
    st.subheader("Convenience bundles")
    st.write("Example groupings only. They are not medical recommendations or derived from real purchase history.")
    cols = st.columns(2)
    for i,(bundle_name,items) in enumerate(BUNDLES.items()):
        with cols[i%2]:
            with st.container(border=True):
                bundle_image = {
                    "First-Aid Basics": "first_aid_bandage.png",
                    "Hydration Supplies": "ors_packet.png",
                    "Home Monitoring": "digital_thermometer.png",
                    "Everyday Personal Care": "petroleum_jelly.png",
                }.get(bundle_name)
                bundle_image_path = asset_path(bundle_image) if bundle_image else None
                if bundle_image_path:
                    st.image(bundle_image_path, use_container_width=True)
                st.markdown(f"#### {bundle_name}")
                total = sum(PRODUCTS[n]["price"]*q for n,q in items.items())
                st.markdown(f"**Sample bundle total: {money(total*0.95)}**")
                st.caption("Includes an illustrative 5% bundle discount.")
                for name,qty in items.items():
                    st.write(f"- {name} × {qty}")
                st.button(
                    "Add bundle to cart",
                    key="bundle_" + bundle_name,
                    use_container_width=True,
                    on_click=add_bundle,
                    args=(items,),
                )
    st.info("A genuine frequently-bought-together feature would require anonymised transaction data. This prototype uses predefined bundles.")

with compare_tab:
    st.subheader("Compare estimated basket prices")
    st.warning("Provider prices are sample estimates derived from MediBill catalogue prices. They are not live or verified quotes.")
    selected = st.multiselect("Select products to compare", list(PRODUCTS),
                              default=["Dolo 650","Electral","Band-Aid"])
    if selected:
        rows = []
        for name in selected:
            p = PRODUCTS[name]
            row = {"Product":name,"Company":p["company"]}
            for provider,multiplier in PROVIDERS.items():
                row[provider] = round(p["price"]*multiplier,2)
            row["Lowest sample price"] = min(round(p["price"]*m,2) for m in PROVIDERS.values())
            rows.append(row)
        df = pd.DataFrame(rows)
        st.dataframe(df.style.format({c:"₹{:.2f}" for c in df.columns if c not in ("Product","Company")}),
                     hide_index=True, use_container_width=True)
        totals = {provider:sum(round(PRODUCTS[n]["price"]*mult,2) for n in selected)
                  for provider,mult in PROVIDERS.items()}
        st.markdown("#### Basket total by provider")
        cols = st.columns(len(totals))
        for i,(provider,total) in enumerate(totals.items()):
            with cols[i]:
                st.metric(provider,money(total))
        cheapest = min(totals,key=totals.get)
        st.success(f"Lowest sample basket: {cheapest} · {money(totals[cheapest])}")
    st.caption("For a fair comparison, verify exact brand, strength, pack size, seller, availability, discounts, delivery fee and date.")
    cols = st.columns(3)
    for i,(label,url) in enumerate([("Tata 1mg","https://www.1mg.com/"),("PharmEasy","https://pharmeasy.in/"),("Apollo 24|7","https://www.apollo247.com/")]):
        with cols[i]:
            st.link_button("Open "+label,url,use_container_width=True)

with pharmacy_tab:
    st.subheader("Nearby pharmacies")
    search_location = st.text_input("Area or PIN code", value=location, key="map_location")
    st.write("Opens a Google Maps search. MediBill does not read GPS or verify opening hours, stock or distance.")
    st.link_button("Search pharmacies on Google Maps", maps_url(search_location), use_container_width=True)
    st.markdown("#### Online pharmacy websites")
