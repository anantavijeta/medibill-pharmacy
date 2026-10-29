import streamlit as st
import pandas as pd
from urllib.parse import quote_plus
from datetime import datetime

# MediBill: educational pharmacy billing and price-comparison prototype.
# Competitor prices and catalogue prices below are illustrative, not live quotes.

st.set_page_config(page_title="MediBill | Smart Pharmacy", layout="wide")

NAVY, BLUE, TEAL = "#17324D", "#2563EB", "#0F766E"
BORDER, TEXT, MUTED, BG = "#DCE4ED", "#1E293B", "#64748B", "#F8FAFC"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {{font-family:Inter,sans-serif;color:{TEXT};}}
.stApp {{background:{BG};}}
[data-testid="stSidebar"] {{background:#F1F5F9;border-right:1px solid {BORDER};}}
.hero {{padding:1.5rem 1.7rem;border-radius:18px;color:white;
background:linear-gradient(115deg,{NAVY},#244C72 62%,{TEAL});margin-bottom:1.2rem;}}
.hero h1 {{color:white;font-size:2.2rem;margin:0 0 .3rem 0;}}
.hero p {{color:#E2E8F0;margin:0;}}
.price {{font-size:1.55rem;font-weight:800;color:{NAVY};}}
.small-muted {{color:{MUTED};font-size:.86rem;}}
div[data-testid="stMetric"] {{background:white;border:1px solid {BORDER};padding:.8rem 1rem;border-radius:12px;}}
div.stButton>button, div.stDownloadButton>button {{border-radius:9px;font-weight:600;min-height:2.5rem;}}
</style>
<div class="hero"><h1>MediBill</h1>
<p>Build your order, compare sample prices, choose delivery, and watch your bill update instantly.</p></div>
""", unsafe_allow_html=True)

PRODUCTS = {
    "Paracetamol 500 mg (10 tablets)": {"price": 30.0, "category": "Pain relief", "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=700&q=80"},
    "Cetirizine 10 mg (10 tablets)": {"price": 45.0, "category": "Allergy care", "image": "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?auto=format&fit=crop&w=700&q=80"},
    "ORS Sachets (1 pack)": {"price": 25.0, "category": "Hydration", "image": "https://images.unsplash.com/photo-1559757175-0eb30cd8c063?auto=format&fit=crop&w=700&q=80"},
    "Vitamin C Tablets (pack)": {"price": 80.0, "category": "Supplements", "image": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?auto=format&fit=crop&w=700&q=80"},
    "Antacid Tablets (pack)": {"price": 55.0, "category": "Digestive care", "image": "https://images.unsplash.com/photo-1607619056574-7b8d3ee536b2?auto=format&fit=crop&w=700&q=80"},
    "Bandage Pack": {"price": 40.0, "category": "First aid", "image": "https://images.unsplash.com/photo-1603398938378-e54eab446dde?auto=format&fit=crop&w=700&q=80"},
    "Digital Thermometer": {"price": 150.0, "category": "Health devices", "image": "https://images.unsplash.com/photo-1584634731339-252c581abfc5?auto=format&fit=crop&w=700&q=80"},
}

# Manually defined bundles stand in for recommendations from purchase history.
BUNDLES = {
    "Basic First-Aid Kit": {"items": {"Bandage Pack": 1, "Digital Thermometer": 1}, "discount": .05,
                            "description": "A practical home first-aid supply bundle."},
    "Hydration Essentials": {"items": {"ORS Sachets (1 pack)": 2, "Digital Thermometer": 1}, "discount": .05,
                             "description": "A convenience grouping of hydration and monitoring items."},
    "Everyday Care Bundle": {"items": {"Bandage Pack": 1, "Vitamin C Tablets (pack)": 1}, "discount": .05,
                             "description": "A sample convenience bundle. Check product suitability separately."},
}

# Placeholder comparison prices: replace with verified same-pack-size prices before presenting as real data.
COMPARISON = {
    "MediBill demo": {"Paracetamol 500 mg (10 tablets)": 30, "Cetirizine 10 mg (10 tablets)": 45, "ORS Sachets (1 pack)": 25, "Vitamin C Tablets (pack)": 80, "Antacid Tablets (pack)": 55, "Bandage Pack": 40, "Digital Thermometer": 150},
    "Tata 1mg (sample)": {"Paracetamol 500 mg (10 tablets)": 32, "Cetirizine 10 mg (10 tablets)": 42, "ORS Sachets (1 pack)": 27, "Vitamin C Tablets (pack)": 76, "Antacid Tablets (pack)": 58, "Bandage Pack": 43, "Digital Thermometer": 145},
    "PharmEasy (sample)": {"Paracetamol 500 mg (10 tablets)": 29, "Cetirizine 10 mg (10 tablets)": 44, "ORS Sachets (1 pack)": 26, "Vitamin C Tablets (pack)": 82, "Antacid Tablets (pack)": 53, "Bandage Pack": 38, "Digital Thermometer": 155},
    "Apollo 24|7 (sample)": {"Paracetamol 500 mg (10 tablets)": 31, "Cetirizine 10 mg (10 tablets)": 46, "ORS Sachets (1 pack)": 24, "Vitamin C Tablets (pack)": 79, "Antacid Tablets (pack)": 56, "Bandage Pack": 41, "Digital Thermometer": 148},
}

DELIVERY = {
    "Standard delivery (2–4 hours)": 25.0,
    "Express delivery (within 90 minutes)": 60.0,
    "Scheduled delivery": 20.0,
    "Store pickup": 0.0,
}

def money(value):
    """Format an amount as Indian rupees."""
    return f"₹{value:,.2f}"

def calculate_bill(cart, discount_rate, delivery_fee, membership):
    """Calculate subtotal, percentage discount, membership benefit, delivery and total."""
    subtotal = sum(PRODUCTS[name]["price"] * qty for name, qty in cart.items())
    discount = subtotal * discount_rate
    after_discount = subtotal - discount
    member_benefit = min(10.0, after_discount) if membership else 0.0
    total = max(0.0, after_discount - member_benefit + delivery_fee)
    return {"subtotal": subtotal, "discount": discount, "membership": member_benefit,
            "delivery": delivery_fee, "total": total}

def maps_url(location):
    """Build a Google Maps search link; this does not access device GPS."""
    search = f"pharmacies near {location}" if location.strip() else "pharmacies near me"
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(search)

def add_bundle(items):
    """Add bundle items to current quantities without exceeding 100 per product."""
    for product, amount in items.items():
        key = "qty_" + product
        st.session_state[key] = min(100, int(st.session_state.get(key, 0)) + amount)

for product in PRODUCTS:
    if "qty_" + product not in st.session_state:
        st.session_state["qty_" + product] = 0

with st.sidebar:
    st.markdown("### Order settings")
    discount_choice = st.selectbox("Discount", ["No discount", "5% off", "10% off"])
    discount_rate = {"No discount": 0.0, "5% off": .05, "10% off": .10}[discount_choice]
    membership = st.checkbox("Apply membership benefit (₹10 off)")
    delivery_method = st.selectbox("Delivery method", list(DELIVERY.keys()))
    delivery_fee = DELIVERY[delivery_method]
    st.caption(f"Sample delivery fee: {money(delivery_fee)}")
    st.markdown("---")
    location = st.text_input("Area or PIN code", placeholder="e.g., Sonipat or 131001")
    st.link_button("Find nearby pharmacies", maps_url(location), use_container_width=True)
    st.caption("Opens Google Maps. Pharmacy results and opening hours are not provided by MediBill.")

shop_tab, bundles_tab, compare_tab, pharmacy_tab = st.tabs(
    ["Shop & live receipt", "Bundles", "Price comparison", "Nearby pharmacies"]
)

with shop_tab:
    st.subheader("Choose products")
    st.write("Change quantities. The receipt on the right updates automatically.")
    products_col, receipt_col = st.columns([1.5, 1], gap="large")
    with products_col:
        names = list(PRODUCTS.keys())
        for i in range(0, len(names), 2):
            row_cols = st.columns(2, gap="medium")
            for j, name in enumerate(names[i:i+2]):
                item = PRODUCTS[name]
                with row_cols[j]:
                    with st.container(border=True):
                        try:
                            st.image(item["image"], use_container_width=True)
                        except Exception:
                            st.caption("Product image unavailable")
                        st.markdown(f"**{name}**")
                        st.caption(item["category"])
                        st.markdown(f"<div class='price'>{money(item['price'])}</div>", unsafe_allow_html=True)
                        st.number_input("Quantity", min_value=0, max_value=100, step=1,
                                        key="qty_" + name, help="Set quantity to 0 to remove.")
    with receipt_col:
        cart = {name: int(st.session_state["qty_" + name]) for name in PRODUCTS
                if int(st.session_state["qty_" + name]) > 0}
        bill = calculate_bill(cart, discount_rate, delivery_fee, membership)
        st.markdown("### Live receipt")
        st.caption("Always visible while you build your order.")
        if cart:
            rows = [{"Item": name, "Qty": qty, "Unit price": money(PRODUCTS[name]["price"]),
                     "Amount": money(PRODUCTS[name]["price"] * qty)} for name, qty in cart.items()]
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            st.info("Your cart is empty. Add a product to begin.")
        st.markdown("---")
        st.metric("Subtotal", money(bill["subtotal"]))
        st.write(f"Discount ({discount_choice}): **−{money(bill['discount'])}**")
        st.write(f"Membership benefit: **−{money(bill['membership'])}**")
        st.write(f"Delivery ({delivery_method}): **{money(bill['delivery'])}**")
        st.markdown(f"<div style='background:white;border:1px solid {BORDER};padding:1rem;border-radius:12px;'>"
                    f"<div style='color:{MUTED};font-size:.85rem;'>TOTAL TO PAY</div>"
                    f"<div class='price'>{money(bill['total'])}</div></div>", unsafe_allow_html=True)
        if cart:
            export_rows = rows + [
                {"Item": "Subtotal", "Qty": "", "Unit price": "", "Amount": money(bill["subtotal"])},
                {"Item": "Discount", "Qty": "", "Unit price": "", "Amount": money(-bill["discount"])},
                {"Item": "Membership benefit", "Qty": "", "Unit price": "", "Amount": money(-bill["membership"])},
                {"Item": "Delivery: " + delivery_method, "Qty": "", "Unit price": "", "Amount": money(bill["delivery"])},
                {"Item": "TOTAL", "Qty": "", "Unit price": "", "Amount": money(bill["total"])},
            ]
            st.download_button("Download receipt (CSV)", pd.DataFrame(export_rows).to_csv(index=False).encode("utf-8"),
                               file_name=f"medibill_receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                               mime="text/csv", use_container_width=True)
        if st.button("Clear entire cart", use_container_width=True):
            for name in PRODUCTS:
                st.session_state["qty_" + name] = 0
            st.rerun()

with bundles_tab:
    st.subheader("Frequently bought together: sample bundles")
    st.write("These are manually configured demo bundles, not recommendations derived from actual purchase history.")
    cols = st.columns(3)
    for i, (bundle_name, bundle) in enumerate(BUNDLES.items()):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"#### {bundle_name}")
                st.write(bundle["description"])
                base = sum(PRODUCTS[p]["price"] * qty for p, qty in bundle["items"].items())
                st.markdown(f"**Bundle price: {money(base * (1-bundle['discount']))}**")
                st.caption("Includes a 5% illustrative bundle discount.")
                for product, qty in bundle["items"].items():
                    st.write(f"- {product} × {qty}")
                if st.button("Add bundle to cart", key="bundle_" + bundle_name, use_container_width=True):
                    add_bundle(bundle["items"])
                    st.success("Bundle items added. Open Shop & live receipt to review.")
    st.info("A production version could calculate frequent item pairs from anonymised order history. This demo has no transaction database.")

with compare_tab:
    st.subheader("Compare estimated basket costs")
    st.warning("All competitor figures below are placeholders for demonstrating the comparison feature. They are not live or verified prices.")
    selected = st.multiselect("Select products", list(PRODUCTS.keys()),
                               default=["Paracetamol 500 mg (10 tablets)", "ORS Sachets (1 pack)"])
    if selected:
        comparison_rows = []
        for product in selected:
            row = {"Product": product}
            for provider, prices in COMPARISON.items():
                row[provider] = prices[product]
            row["Lowest sample price"] = min(prices[product] for prices in COMPARISON.values())
            comparison_rows.append(row)
        comparison_df = pd.DataFrame(comparison_rows)
        st.dataframe(comparison_df.style.format({c: "₹{:.2f}" for c in comparison_df.columns if c != "Product"}),
                     hide_index=True, use_container_width=True)
        totals = {provider: sum(prices[p] for p in selected) for provider, prices in COMPARISON.items()}
        st.markdown("#### Total for selected sample basket")
        cols = st.columns(len(totals))
        for i, (provider, total) in enumerate(totals.items()):
            with cols[i]:
                st.metric(provider, money(total))
        cheapest = min(totals, key=totals.get)
        st.success(f"Lowest sample basket: {cheapest} at {money(totals[cheapest])}. Placeholder prices only; delivery and live offers are excluded.")
    st.caption("For a fair comparison, verify the exact brand, strength, pack size, seller, stock, discounts, delivery fee, and date.")
    links = [("Tata 1mg", "https://www.1mg.com/"), ("PharmEasy", "https://pharmeasy.in/"),
             ("Apollo 24|7", "https://www.apollo247.com/")]
    link_cols = st.columns(3)
    for i, (label, url) in enumerate(links):
        with link_cols[i]:
            st.link_button("Open " + label, url, use_container_width=True)

with pharmacy_tab:
    st.subheader("Nearby pharmacies")
    pharmacy_location = st.text_input("Area or PIN code for pharmacy search", value=location,
                                       placeholder="Enter area or PIN code", key="pharmacy_location")
    st.write("Search nearby pharmacies through Google Maps. MediBill does not access your GPS or verify pharmacy stock.")
    st.link_button("Search Google Maps for pharmacies", maps_url(pharmacy_location), use_container_width=True)
    st.markdown("#### Online pharmacy websites")
    st.markdown("- [Tata 1mg](https://www.1mg.com/)")
    st.markdown("- [PharmEasy](https://pharmeasy.in/)")
    st.markdown("- [Apollo 24|7](https://www.apollo247.com/)")

st.markdown("---")
st.caption("MediBill is an academic prototype. Catalogue prices, competitor estimates, discounts, bundles, and delivery fees are illustrative. Confirm product details, current prices, stock, and delivery directly with the provider. This application does not provide medical advice.")
