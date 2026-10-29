import streamlit as st
import pandas as pd
from urllib.parse import quote
from datetime import datetime

# MediBill is an academic demo. Prices, provider comparisons, bundles and delivery
# fees below are sample data, not live offers, medical advice, or real sales analytics.
st.set_page_config(page_title="MediBill | Pharmacy Comparison", layout="wide")

NAVY, BLUE, TEAL = "#17324D", "#2F6690", "#3A7D78"
PRODUCTS = {
    "Paracetamol 500 mg": {"price": 30, "category": "Pain and fever relief", "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=700&q=80", "note": "Follow the product label or qualified professional's advice."},
    "Cetirizine 10 mg": {"price": 45, "category": "Allergy relief", "image": "https://images.unsplash.com/photo-1607619056574-7b8d3ee536b2?auto=format&fit=crop&w=700&q=80", "note": "Check the label for warnings and suitability."},
    "ORS Sachets": {"price": 25, "category": "Hydration support", "image": "https://images.unsplash.com/photo-1550572017-edd951b55104?auto=format&fit=crop&w=700&q=80", "note": "Prepare according to the package instructions."},
    "Vitamin C Tablets": {"price": 80, "category": "Vitamin supplement", "image": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?auto=format&fit=crop&w=700&q=80", "note": "Supplements are not a substitute for a balanced diet."},
    "Antacid Tablets": {"price": 55, "category": "Digestive care", "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=700&q=80", "note": "Follow package directions; seek advice if symptoms persist."},
    "Bandage Pack": {"price": 40, "category": "First aid", "image": "https://images.unsplash.com/photo-1603398938378-e54eab446dde?auto=format&fit=crop&w=700&q=80", "note": "For basic first-aid use."},
    "Digital Thermometer": {"price": 150, "category": "Health monitoring", "image": "https://images.unsplash.com/photo-1584634731339-252c581abfc5?auto=format&fit=crop&w=700&q=80", "note": "Read the device instructions before use."},
}
# Fictional benchmark providers and illustrative prices. Replace with verified live data before claiming real comparisons.
PROVIDER_PRICES = {
    "Paracetamol 500 mg": {"MediBill Demo": 30, "Pharmacy A (sample)": 28, "Pharmacy B (sample)": 32, "Pharmacy C (sample)": 35},
    "Cetirizine 10 mg": {"MediBill Demo": 45, "Pharmacy A (sample)": 42, "Pharmacy B (sample)": 48, "Pharmacy C (sample)": 44},
    "ORS Sachets": {"MediBill Demo": 25, "Pharmacy A (sample)": 24, "Pharmacy B (sample)": 27, "Pharmacy C (sample)": 22},
    "Vitamin C Tablets": {"MediBill Demo": 80, "Pharmacy A (sample)": 76, "Pharmacy B (sample)": 82, "Pharmacy C (sample)": 75},
    "Antacid Tablets": {"MediBill Demo": 55, "Pharmacy A (sample)": 53, "Pharmacy B (sample)": 57, "Pharmacy C (sample)": 50},
    "Bandage Pack": {"MediBill Demo": 40, "Pharmacy A (sample)": 38, "Pharmacy B (sample)": 42, "Pharmacy C (sample)": 36},
    "Digital Thermometer": {"MediBill Demo": 150, "Pharmacy A (sample)": 145, "Pharmacy B (sample)": 155, "Pharmacy C (sample)": 139},
}
DELIVERY = {
    "Standard delivery": {"fee": 30, "eta": "Illustrative estimate: 3–6 hours, where available"},
    "Express delivery": {"fee": 60, "eta": "Illustrative estimate: 60–120 minutes, where available"},
    "Pickup from pharmacy": {"fee": 0, "eta": "Collect from selected pharmacy"},
    "Scheduled delivery": {"fee": 20, "eta": "Illustrative scheduled-delivery fee"},
}
BUNDLES = [
    {"name": "Basic First-Aid Kit", "items": {"Bandage Pack": 1, "Digital Thermometer": 1}, "desc": "Basic first-aid and temperature-monitoring supplies."},
    {"name": "Hydration Support Pair", "items": {"ORS Sachets": 2, "Digital Thermometer": 1}, "desc": "A demonstration bundle for hydration supplies and temperature monitoring."},
    {"name": "Everyday Essentials", "items": {"Paracetamol 500 mg": 1, "Bandage Pack": 1, "ORS Sachets": 1}, "desc": "A small mix of general health and first-aid essentials."},
]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] {{font-family:'DM Sans',sans-serif;}}
.stApp {{background:#F3F7FA;}}
.block-container {{max-width:1400px;padding-top:1.5rem;padding-bottom:3rem;}}
h1,h2,h3 {{font-family:'Manrope',sans-serif;color:{NAVY};letter-spacing:-.02em;}}
.hero {{background:linear-gradient(115deg,{NAVY},{BLUE},{TEAL});border-radius:18px;padding:30px 34px;color:white;margin-bottom:18px;}}
.hero h1 {{color:white;font-size:2.4rem;margin:0 0 8px 0;}}
.hero p {{color:#E7F0F5;margin:0;max-width:800px;}}
.eyebrow {{font-size:.72rem;letter-spacing:.15em;text-transform:uppercase;color:#B9D7E4;font-weight:700;margin-bottom:8px;}}
.card {{background:white;border:1px solid #DCE5EC;border-radius:15px;padding:16px;margin-bottom:12px;}}
div[data-testid="stMetric"] {{background:white;border:1px solid #DCE5EC;border-radius:13px;padding:13px;}}
div[data-testid="stMetricValue"] {{color:{NAVY};font-family:'Manrope',sans-serif;}}
.stButton>button,.stDownloadButton>button {{border-radius:9px;font-weight:700;min-height:2.5rem;}}
[data-testid="stSidebar"] {{background:white;border-right:1px solid #DCE5EC;}}
</style>
<div class="hero">
<div class="eyebrow">Pharmacy shopping, made clearer</div>
<h1>MediBill</h1>
<p>Build a basket, estimate your bill, compare sample prices, choose delivery, and find nearby pharmacies from one clean dashboard.</p>
</div>
""", unsafe_allow_html=True)

st.caption("Academic prototype. Prices, provider comparisons, bundle patterns, delivery fees and timings are sample data, not live marketplace offers. Confirm actual availability, prices, product details and suitability with a licensed pharmacy.")

def money(value):
    return f"₹{value:,.2f}"

def calculate_bill(items, discount_rate, delivery_fee, membership):
    # Add each selected product's price multiplied by its quantity.
    subtotal = sum(PRODUCTS[name]["price"] * qty for name, qty in items.items())
    discount = subtotal * discount_rate
    after_discount = subtotal - discount
    # Membership benefit cannot exceed the amount remaining after discount.
    member_benefit = min(10, after_discount) if membership else 0
    total = max(0, after_discount - member_benefit + delivery_fee)
    return {"subtotal": subtotal, "discount": discount, "membership": member_benefit, "delivery": delivery_fee, "total": total}

def map_url(provider, query):
    if provider == "Google Maps":
        return "https://www.google.com/maps/search/" + quote(query)
    return "https://www.openstreetmap.org/search?query=" + quote(query)

# Persistent sidebar inputs.
with st.sidebar:
    st.markdown("## Build your basket")
    basket = {}
    for i, name in enumerate(PRODUCTS, start=1):
        if st.checkbox(name, key=f"item_{i}"):
            basket[name] = int(st.number_input(f"Quantity: {name}", 1, 100, 1, key=f"qty_{i}"))
    discount_name = st.selectbox("Discount", ["No discount", "5% discount", "10% discount"])
    discount_rate = {"No discount": 0, "5% discount": .05, "10% discount": .10}[discount_name]
    membership = st.checkbox("Membership benefit (₹10)")
    delivery_name = st.selectbox("Delivery method", list(DELIVERY))
    delivery_fee = DELIVERY[delivery_name]["fee"]
    st.caption(DELIVERY[delivery_name]["eta"])
    st.caption("Product prices are illustrative demo values.")

bill = calculate_bill(basket, discount_rate, delivery_fee, membership)
tabs = st.tabs(["Bill builder", "Price comparison", "Nearby pharmacies", "Bundles", "Project details"])

with tabs[0]:
    st.subheader("Your basket")
    if not basket:
        st.info("Select products and quantities in the left panel to build your basket.")
    else:
        col1, col2 = st.columns([1.5, 1], gap="large")
        with col1:
            rows = []
            for name, qty in basket.items():
                p = PRODUCTS[name]
                image_col, details_col, price_col = st.columns([.8, 2.2, 1])
                with image_col:
                    st.image(p["image"], width=85)
                with details_col:
                    st.markdown(f"**{name}**")
                    st.caption(p["category"])
                    st.caption(p["note"])
                with price_col:
                    st.markdown(f"**{money(p['price'] * qty)}**")
                    st.caption(f"{qty} × {money(p['price'])}")
                rows.append({"Product": name, "Quantity": qty, "Unit price (₹)": p["price"], "Line total (₹)": p["price"] * qty})
                st.divider()
            receipt = pd.DataFrame(rows)
            st.markdown("#### Itemized receipt")
            st.dataframe(receipt, use_container_width=True, hide_index=True)
            st.download_button("Download receipt CSV", receipt.to_csv(index=False).encode("utf-8"),
                file_name=f"medibill_receipt_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Bill summary")
            st.metric("Subtotal", money(bill["subtotal"]))
            st.metric("Discount", "− " + money(bill["discount"]))
            st.metric("Membership benefit", "− " + money(bill["membership"]))
            st.metric("Delivery fee", money(bill["delivery"]))
            st.markdown("---")
            st.markdown("#### Estimated total")
            st.markdown(f"<h1 style='color:{NAVY};'>{money(bill['total'])}</h1>", unsafe_allow_html=True)
            st.caption(f"Selected delivery: {delivery_name}")
            st.markdown("</div>", unsafe_allow_html=True)
            st.success("Estimate calculated. Confirm the final payable amount with the provider.")

    st.markdown("#### Product catalogue")
    cols = st.columns(3)
    for i, (name, p) in enumerate(PRODUCTS.items()):
        with cols[i % 3]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.image(p["image"], use_container_width=True)
            st.markdown(f"**{name}**")
            st.caption(p["category"])
            st.markdown(f"### {money(p['price'])}")
            st.caption(p["note"])
            st.markdown("</div>", unsafe_allow_html=True)

with tabs[1]:
    st.subheader("Compare estimated product prices")
    st.write("Choose a product to compare its demo price with fictional provider benchmarks.")
    product = st.selectbox("Product", list(PROVIDER_PRICES))
    comparison = pd.DataFrame([{"Provider": k, "Sample unit price (₹)": v} for k, v in PROVIDER_PRICES[product].items()])
    comparison = comparison.sort_values("Sample unit price (₹)").reset_index(drop=True)
    comparison["Difference vs MediBill Demo (₹)"] = comparison["Sample unit price (₹)"] - PROVIDER_PRICES[product]["MediBill Demo"]
    lowest = comparison.iloc[0]
    a, b, c = st.columns(3)
    a.metric("Lowest sample price", money(float(lowest["Sample unit price (₹)"])))
    b.metric("Lowest sample provider", str(lowest["Provider"]))
    c.metric("MediBill demo price", money(PROVIDER_PRICES[product]["MediBill Demo"]))
    st.dataframe(comparison, use_container_width=True, hide_index=True)
    st.bar_chart(comparison.set_index("Provider")[["Sample unit price (₹)"]])
    st.warning("Provider labels and prices are fictional. They are not verified prices from Tata 1mg, PharmEasy, Apollo, Netmeds or local pharmacies.")
    st.markdown("**To make this a real comparison:** use the same brand, strength and pack size; record source URLs and date/time checked; include delivery fees and coupon conditions; compare final payable totals.")

with tabs[2]:
    st.subheader("Find nearby pharmacies")
    st.write("Enter a locality, landmark, PIN code or city. MediBill opens a map search rather than claiming to have live GPS or pharmacy inventory.")
    location = st.text_input("Your area or PIN code", placeholder="For example: Sector 14, Sonipat or 131001")
    search_type = st.selectbox("Search for", ["Pharmacies", "24-hour pharmacies", "Pharmacies with delivery", "Medical stores"])
    if location.strip():
        query = f"{search_type} near {location.strip()}"
        c1, c2 = st.columns(2)
        with c1:
            st.link_button("Open Google Maps results", map_url("Google Maps", query), use_container_width=True)
        with c2:
            st.link_button("Open OpenStreetMap results", map_url("OpenStreetMap", query), use_container_width=True)
        st.info("Map information can be incomplete. Call the pharmacy to confirm hours, stock, prescription requirements, delivery area and final price.")
    else:
        st.info("Enter your area or PIN code to create map links.")
    st.markdown("#### Delivery methods")
    st.dataframe(pd.DataFrame([{"Method": k, "Illustrative fee (₹)": v["fee"], "Timing / notes": v["eta"]} for k, v in DELIVERY.items()]), use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("Frequently bought together and package ideas")
    st.write("These are rule-based demo bundles, not recommendations based on real customer purchase history. They are not medical recommendations.")
    for bundle in BUNDLES:
        with st.container(border=True):
            left, right = st.columns([2, 1])
            subtotal = sum(PRODUCTS[n]["price"] * q for n, q in bundle["items"].items())
            discounted = subtotal * .95
            with left:
                st.markdown(f"### {bundle['name']}")
                st.write(bundle["desc"])
                for n, q in bundle["items"].items():
                    st.write(f"- {n} × {q} · {money(PRODUCTS[n]['price'] * q)}")
                st.caption("The 5% bundle discount is hypothetical.")
            with right:
                st.metric("Regular total", money(subtotal))
                st.metric("Sample bundle price", money(discounted))
                st.caption(f"Sample saving: {money(subtotal - discounted)}")
                if st.button("Add bundle to basket", key="bundle_" + bundle["name"]):
                    for n, q in bundle["items"].items():
                        index = list(PRODUCTS).index(n) + 1
                        st.session_state[f"item_{index}"] = True
                        st.session_state[f"qty_{index}"] = q
                    st.rerun()

with tabs[4]:
    st.subheader("About MediBill")
    st.write("MediBill is an academic Python and Streamlit prototype for estimating a pharmacy basket total. It demonstrates dictionaries, lists, functions, loops, conditionals, arithmetic, tables and CSV export.")
    st.markdown("#### Interface improvements")
    st.markdown("- Professional navy, blue and teal colour palette.\n- Product images and clearer catalogue cards.\n- Persistent basket controls and itemized receipt.\n- Separate price comparison, pharmacy search and bundle sections.\n- Delivery choices for standard, express, pickup and scheduled orders.")
    st.markdown("#### Limitations")
    st.markdown("- Prices, provider benchmarks, delivery fees and bundle patterns are sample data.\n- Pharmacy searches use external map results and do not guarantee stock or opening hours.\n- No payment processing, user accounts, inventory database, order history, or medical advice.")
    st.markdown("#### Suggested next improvements")
    st.markdown("- Replace sample comparison values with verified prices and source links.\n- Add automated tests for discounts, membership limits, delivery and empty baskets.\n- Capture screenshots of the running app for the project report.\n- Keep the main application in one `app.py` file to match the assignment instructions.")

st.markdown("---")
st.caption("MediBill · Academic prototype · Confirm all prices, availability and product information with a pharmacy before purchase.")
