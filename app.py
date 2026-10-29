
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus
import html

# ============================================================
# MEDIBILL | PHARMACY BILLING APPLICATION
# ============================================================

st.set_page_config(
    page_title="MediBill | Pharmacy Billing",
    page_icon="💊",
    layout="wide"
)

# -------------------- DESIGN SETTINGS ------------------------

NAVY = "#17324D"
BLUE = "#2563EB"
TEAL = "#0F766E"
BACKGROUND = "#F4F6F9"
PAPER = "#FFFDF2"
BORDER = "#D7DEE7"

APP_DIR = Path(__file__).resolve().parent
ASSET_DIR = APP_DIR / "assets"


def asset_path(filename):
    """Find images in the repository root or assets folder."""
    if not filename:
        return None

    for folder in (APP_DIR, ASSET_DIR):
        path = folder / filename
        if path.is_file():
            return str(path)

    return None


# -------------------- CSS DESIGN -----------------------------

st.markdown(
    f"""
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    .stApp {{
        background-color: {BACKGROUND};
    }}

    html, body, [class*="css"] {{
        font-family: Inter, sans-serif;
    }}

    [data-testid="stSidebar"] {{
        background-color: #EDF2F7;
    }}

    .hero {{
        background: linear-gradient(120deg, {NAVY}, #244C72, {TEAL});
        color: white;
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 18px;
    }}

    .hero h1 {{
        color: white;
        font-size: 36px;
        margin-bottom: 5px;
    }}

    .hero p {{
        color: #E6EDF5;
        margin-bottom: 0;
    }}

    div[data-testid="stMetric"] {{
        background: white;
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 12px;
    }}

    .paper-bill {{
        background: {PAPER};
        color: #292820;
        border: 1px solid #C9C4AA;
        padding: 18px;
        border-radius: 3px;
        font-family: "Courier New", monospace;
        box-shadow: 0 3px 12px #00000012;
        overflow-x: auto;
    }}

    .paper-title {{
        text-align: center;
        font-weight: bold;
        font-size: 19px;
        letter-spacing: 2px;
    }}

    .paper-subtitle {{
        text-align: center;
        font-size: 10px;
        margin: 4px 0;
    }}

    .paper-line {{
        border-top: 1px dashed #77745F;
        margin: 10px 0;
    }}

    .paper-meta {{
        display: flex;
        justify-content: space-between;
        gap: 8px;
        font-size: 10px;
        margin: 5px 0;
    }}

    .paper-bill table {{
        width: 100%;
        border-collapse: collapse;
        font-family: "Courier New", monospace;
        font-size: 10px;
        margin-top: 8px;
    }}

    .paper-bill th {{
        border-top: 1px solid #77745F;
        border-bottom: 1px solid #77745F;
        text-align: left;
        padding: 6px 3px;
    }}

    .paper-bill td {{
        padding: 6px 3px;
        border-bottom: 1px dotted #C9C4AA;
        vertical-align: top;
    }}

    .paper-bill .num {{
        text-align: right;
        white-space: nowrap;
    }}

    .paper-total {{
        text-align: right;
        font-weight: bold;
        font-size: 15px;
        margin-top: 10px;
    }}

    .small-note {{
        font-size: 10px;
        line-height: 1.5;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# IMAGE CATALOGUE
# ============================================================

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
    "Topical care": "medicine_blister_packs.png",
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
    "Wellness": "vitamin_c.png",
    "Baby care": "petroleum_jelly.png",
    "Nasal care": "medicine_capsules.png",
}


# ============================================================
# PRODUCT DATABASE
# Prices are illustrative for an academic demonstration.
# ============================================================

RAW_PRODUCTS = [
    ("Dolo 650", "Paracetamol 650 mg", "Micro Labs", "Pain relief", 32),
    ("Calpol 500", "Paracetamol 500 mg", "GSK", "Pain relief", 24),
    ("Crocin Advance", "Paracetamol 500 mg", "Haleon", "Pain relief", 28),
    ("Combiflam", "Ibuprofen + Paracetamol", "Sanofi", "Pain relief", 42),
    ("Ibugesic", "Ibuprofen", "Cipla", "Pain relief", 38),
    ("Moov Spray", "Topical pain relief", "Reckitt", "Topical care", 145),
    ("Volini Gel", "Topical pain relief", "Sun Pharma", "Topical care", 110),
    ("Cetirizine", "Cetirizine 10 mg", "Cipla", "Allergy care", 22),
    ("Okacet", "Cetirizine 10 mg", "Cipla", "Allergy care", 26),
    ("Allegra 120", "Fexofenadine 120 mg", "Sanofi", "Allergy care", 165),
    ("Montair LC", "Montelukast + Levocetirizine", "Cipla", "Allergy care", 190),
    ("Sinarest", "Cold symptom combination", "Centaur", "Cold care", 45),
    ("Vicks Action 500", "Cold symptom combination", "P&G", "Cold care", 48),
    ("Strepsils", "Throat lozenges", "Reckitt", "Throat care", 45),
    ("Honitus", "Cough syrup", "Dabur", "Cough care", 115),
    ("Benadryl Cough Formula", "Cough syrup", "Kenvue", "Cough care", 125),
    ("Ascoril LS", "Cough syrup", "Glenmark", "Cough care", 130),
    ("Digene", "Antacid tablets", "Abbott", "Digestive care", 32),
    ("Gelusil", "Antacid tablets", "Pfizer", "Digestive care", 40),
    ("ENO", "Antacid powder", "Haleon", "Digestive care", 12),
    ("Pudin Hara", "Digestive care", "Dabur", "Digestive care", 38),
    ("Electral", "ORS sachets", "FDC", "Hydration", 22),
    ("ORSL", "Rehydration drink", "Dabur", "Hydration", 35),
    ("Enerzal", "Electrolyte drink", "FDC", "Hydration", 32),
    ("Limcee", "Vitamin C tablets", "Abbott", "Vitamins", 35),
    ("Celin 500", "Vitamin C tablets", "GSK", "Vitamins", 40),
    ("Zincovit", "Multivitamin supplement", "Apex Laboratories", "Vitamins", 105),
    ("Supradyn", "Multivitamin supplement", "Bayer", "Vitamins", 55),
    ("Shelcal 500", "Calcium supplement", "Torrent Pharma", "Vitamins", 125),
    ("Neurobion Forte", "Vitamin supplement", "P&G Health", "Vitamins", 42),
    ("Evion 400", "Vitamin E supplement", "P&G", "Vitamins", 38),
    ("Becosules", "Vitamin supplement", "Pfizer", "Vitamins", 45),
    ("ORS Powder", "Oral rehydration salts", "Demo generic brand", "Hydration", 18),
    ("Betadine Ointment", "Antiseptic ointment", "Win-Medicare", "First aid", 80),
    ("Savlon Antiseptic", "Antiseptic liquid", "ITC", "First aid", 95),
    ("Dettol Antiseptic", "Antiseptic liquid", "Reckitt", "First aid", 90),
    ("Band-Aid", "Adhesive bandages", "Kenvue", "First aid", 45),
    ("Hansaplast", "Adhesive bandages", "Beiersdorf", "First aid", 50),
    ("Cotton Roll", "Medical cotton", "Romsons", "First aid", 38),
    ("Sterile Gauze", "Gauze dressing pack", "Dispovan", "First aid", 55),
    ("Crepe Bandage", "Elastic bandage", "Vissco", "First aid", 95),
    ("Digital Thermometer", "Digital thermometer", "Dr Trust", "Devices", 250),
    ("BP Monitor", "Digital BP monitor", "Omron", "Devices", 1650),
    ("Pulse Oximeter", "Finger pulse oximeter", "BPL", "Devices", 950),
    ("Glucometer Strips", "Test strips pack", "Accu-Chek / Roche", "Devices", 650),
    ("Sugar Free Gold", "Tabletop sweetener", "Zydus Wellness", "Wellness", 95),
    ("Vaseline Petroleum Jelly", "Skin protectant", "Unilever", "Personal care", 65),
    ("Boroline", "Skin cream", "G.D. Pharmaceuticals", "Personal care", 48),
    ("Nivea Creme", "Moisturising cream", "Beiersdorf", "Personal care", 85),
    ("Septilin", "Herbal wellness product", "Himalaya Wellness", "Wellness", 120),
    ("Aloe Vera Gel", "Aloe vera gel", "Patanjali", "Personal care", 90),
    ("Johnson's Baby Powder", "Baby care powder", "Kenvue", "Baby care", 110),
    ("Pampers Diapers", "Baby diaper pack", "P&G", "Baby care", 299),
    ("Johnson's Baby Lotion", "Baby lotion", "Kenvue", "Baby care", 145),
    ("Otrivin Adult", "Nasal spray", "Haleon", "Nasal care", 95),
    ("Nasivion Adult", "Nasal drops", "P&G", "Nasal care", 85),
]

PRODUCTS = {
    name: {
        "generic": generic,
        "company": company,
        "category": category,
        "price": float(price),
    }
    for name, generic, company, category, price in RAW_PRODUCTS
}


# ============================================================
# BUNDLES AND PROVIDER ESTIMATES
# ============================================================

BUNDLES = {
    "First-Aid Basics": {
        "Band-Aid": 1,
        "Sterile Gauze": 1,
        "Betadine Ointment": 1,
    },
    "Hydration Supplies": {
        "Electral": 2,
        "ORSL": 1,
    },
    "Home Monitoring": {
        "Digital Thermometer": 1,
        "Pulse Oximeter": 1,
    },
    "Everyday Personal Care": {
        "Vaseline Petroleum Jelly": 1,
        "Nivea Creme": 1,
    },
}

PROVIDERS = {
    "MediBill demo catalogue": 1.00,
    "Tata 1mg sample estimate": 1.04,
    "PharmEasy sample estimate": 0.97,
    "Apollo 24|7 sample estimate": 1.02,
}

DELIVERY_OPTIONS = {
    "Standard delivery (2–4 hours)": 25.0,
    "Express delivery (within 90 minutes)": 60.0,
    "Scheduled delivery": 20.0,
    "Store pickup": 0.0,
}


# ============================================================
# BILL CALCULATIONS
# ============================================================

def money(value):
    return f"₹{value:,.2f}"


def calculate_bill(cart, discount_rate, delivery_fee, membership, tax_rate):
    subtotal = sum(
        PRODUCTS[name]["price"] * quantity
        for name, quantity in cart.items()
    )

    discount = subtotal * discount_rate
    after_discount = max(0.0, subtotal - discount)

    membership_discount = min(10.0, after_discount) if membership else 0.0

    taxable_amount = max(0.0, after_discount - membership_discount)
    tax = taxable_amount * tax_rate

    # Do not charge delivery if the cart is empty.
    actual_delivery = delivery_fee if cart else 0.0

    total = taxable_amount + tax + actual_delivery

    return {
        "subtotal": subtotal,
        "discount": discount,
        "membership": membership_discount,
        "taxable": taxable_amount,
        "tax": tax,
        "delivery": actual_delivery,
        "total": total,
    }


def create_maps_url(location):
    if location.strip():
        query = "pharmacies near " + location.strip()
    else:
        query = "pharmacies near me"

    return (
        "https://www.google.com/maps/search/?api=1&query="
        + quote_plus(query)
    )


# ============================================================
# RECEIPT HTML
# IMPORTANT: HTML is returned by this function and rendered
# with unsafe_allow_html=True below. Do not paste its output
# separately into the Python file.
# ============================================================

def receipt_html(cart, bill, discount_label, delivery_label, invoice_number):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")

    rows = ""

    for name, quantity in cart.items():
        item = PRODUCTS[name]
        safe_name = html.escape(name)
        safe_company = html.escape(item["company"])

        amount = item["price"] * quantity

        rows += f"""
        <tr>
            <td>
                {safe_name}<br>
                <small>{safe_company}</small>
            </td>
            <td class="num">{quantity}</td>
            <td class="num">{item["price"]:.2f}</td>
            <td class="num">{amount:.2f}</td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
            <td colspan="4" style="text-align:center;padding:18px">
                No items added
            </td>
        </tr>
        """

    safe_invoice = html.escape(invoice_number)
    safe_discount = html.escape(discount_label)
    safe_delivery = html.escape(delivery_label)

    return f"""
    <div class="paper-bill">
        <div class="paper-title">MEDIBILL PHARMACY</div>

        <div class="paper-subtitle">
            SAMPLE BILLING COUNTER
        </div>

        <div class="paper-subtitle">
            Educational demonstration - Not a tax invoice
        </div>

        <div class="paper-line"></div>

        <div class="paper-meta">
            <span>Invoice: {safe_invoice}</span>
            <span>{timestamp}</span>
        </div>

        <div class="paper-meta">
            <span>Customer: Walk-in customer</span>
            <span>Copy: Original</span>
        </div>

        <div class="paper-line"></div>

        <table>
            <thead>
                <tr>
                    <th>Item / Company</th>
                    <th class="num">Qty</th>
                    <th class="num">Rate</th>
                    <th class="num">Amount</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>

        <div class="paper-line"></div>

        <div class="paper-meta">
            <span>Subtotal</span>
            <span>{bill["subtotal"]:.2f}</span>
        </div>

        <div class="paper-meta">
            <span>Discount ({safe_discount})</span>
            <span>-{bill["discount"]:.2f}</span>
        </div>

        <div class="paper-meta">
            <span>Membership benefit</span>
            <span>-{bill["membership"]:.2f}</span>
        </div>

        <div class="paper-meta">
            <span>Illustrative tax</span>
            <span>{bill["tax"]:.2f}</span>
        </div>

        <div class="paper-meta">
            <span>Delivery: {safe_delivery}</span>
            <span>{bill["delivery"]:.2f}</span>
        </div>

        <div class="paper-line"></div>

        <div class="paper-total">
            TOTAL: ₹{bill["total"]:.2f}
        </div>

        <div class="paper-line"></div>

        <div class="small-note">
            Payment status: Not collected
        </div>

        <div class="small-note">
            Live stock, batch, expiry and tax-registration data are not connected.
        </div>

        <div class="small-note" style="text-align:center;margin-top:12px">
            Thank you for using MediBill.
        </div>
    </div>
    """


# ============================================================
# SESSION STATE
# ============================================================

for name in PRODUCTS:
    st.session_state.setdefault("qty_" + name, 0)

st.session_state.setdefault(
    "invoice_no",
    "MB" + datetime.now().strftime("%y%m%d%H%M%S")
)


def add_bundle_to_cart(bundle):
    for name, quantity in bundle.items():
        key = "qty_" + name
        current = int(st.session_state.get(key, 0))
        st.session_state[key] = min(100, current + quantity)


def clear_cart():
    for name in PRODUCTS:
        st.session_state["qty_" + name] = 0

    st.session_state["invoice_no"] = (
        "MB" + datetime.now().strftime("%y%m%d%H%M%S")
    )


# ============================================================
# HOMEPAGE
# ============================================================

banner = asset_path("pharmacy_interior.png")

if banner:
    st.image(banner, use_container_width=True)

st.markdown(
    """
    <div class="hero">
        <h1>💊 MediBill</h1>
        <p>
            Your pharmacy catalogue, smart billing counter,
            basket comparison and paper-style receipt.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric("Catalogue Products", len(PRODUCTS))

with metric2:
    st.metric(
        "Product Categories",
        len({item["category"] for item in PRODUCTS.values()})
    )

with metric3:
    st.metric("Sample Providers", len(PROVIDERS))


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## Order Settings")

    discount_choice = st.selectbox(
        "Discount",
        ["No discount", "5% off", "10% off"]
    )

    discount_rate = {
        "No discount": 0.0,
        "5% off": 0.05,
        "10% off": 0.10,
    }[discount_choice]

    membership = st.checkbox("Membership benefit (up to ₹10 off)")

    delivery_method = st.selectbox(
        "Delivery method",
        list(DELIVERY_OPTIONS.keys())
    )

    delivery_fee = DELIVERY_OPTIONS[delivery_method]

    tax_choice = st.selectbox(
        "Illustrative tax setting",
        ["No tax", "5% demo tax", "12% demo tax"]
    )

    tax_rate = {
        "No tax": 0.0,
        "5% demo tax": 0.05,
        "12% demo tax": 0.12,
    }[tax_choice]

    st.caption("Tax rates are for arithmetic demonstration only.")

    st.markdown("---")
    st.markdown("### Find Nearby Pharmacies")

    location = st.text_input(
        "Area or PIN code",
        placeholder="Enter area or PIN code"
    )

    st.link_button(
        "Search Google Maps",
        create_maps_url(location),
        use_container_width=True
    )


# ============================================================
# APPLICATION TABS
# ============================================================

shop_tab, bundles_tab, compare_tab, pharmacy_tab = st.tabs(
    [
        "Products & Paper Bill",
        "Bundles",
        "Price Comparison",
        "Nearby Pharmacies",
    ]
)


# ============================================================
# TAB 1: PRODUCT CATALOGUE AND RECEIPT
# ============================================================

with shop_tab:

    product_col, receipt_col = st.columns([1.4, 1], gap="large")

    with product_col:
        st.subheader("Product Catalogue")

        search = st.text_input(
            "Search brand, ingredient or company",
            placeholder="e.g. Dolo, Cipla, vitamin"
        )

        categories = ["All categories"] + sorted(
            {item["category"] for item in PRODUCTS.values()}
        )

        selected_category = st.selectbox(
            "Filter by category",
            categories
        )

        filtered_products = []

        for name, item in PRODUCTS.items():
            matches_search = (
                search.lower() in name.lower()
                or search.lower() in item["generic"].lower()
                or search.lower() in item["company"].lower()
            )

            matches_category = (
                selected_category == "All categories"
                or item["category"] == selected_category
            )

            if matches_search and matches_category:
                filtered_products.append(name)

        st.caption(
            f"{len(filtered_products)} products found "
            f"out of {len(PRODUCTS)}"
        )

        if not filtered_products:
            st.warning("No products found. Try a different search.")

        for start in range(0, len(filtered_products), 2):
            columns = st.columns(2)

            for index, name in enumerate(filtered_products[start:start + 2]):
                item = PRODUCTS[name]

                with columns[index]:
                    with st.container(border=True):

                        image_file = (
                            PRODUCT_IMAGES.get(name)
                            or CATEGORY_IMAGES.get(item["category"])
                            or "medicine_blister_packs.png"
                        )

                        image = asset_path(image_file)

                        if image:
                            st.image(image, use_container_width=True)
                        else:
                            st.caption("Product image unavailable")

                        st.markdown(f"**{name}**")
                        st.caption(item["generic"])

                        st.markdown(
                            f"<span style='color:{TEAL};font-weight:700'>"
                            f"{money(item['price'])}</span>",
                            unsafe_allow_html=True
                        )

                        st.caption(
                            f"{item['company']} · {item['category']}"
                        )

                        st.number_input(
                            "Quantity",
                            min_value=0,
                            max_value=100,
                            step=1,
                            key="qty_" + name
                        )

    # Build the cart from the quantities in session state.
    cart = {
        name: int(st.session_state["qty_" + name])
        for name in PRODUCTS
        if int(st.session_state["qty_" + name]) > 0
    }

    bill = calculate_bill(
        cart,
        discount_rate,
        delivery_fee,
        membership,
        tax_rate
    )

    with receipt_col:
        st.subheader("Paper-Style Receipt")

        st.caption(
            "Your receipt updates automatically when quantities or settings change."
        )

        # IMPORTANT: Render the returned HTML as HTML.
        # Do not print receipt_html(...) with st.write().
        st.markdown(
            receipt_html(
                cart,
                bill,
                discount_choice,
                delivery_method,
                st.session_state["invoice_no"]
            ),
            unsafe_allow_html=True
        )

        st.markdown("### Bill Summary")

        st.metric("Subtotal", money(bill["subtotal"]))
        st.metric("Total Discount", money(
            bill["discount"] + bill["membership"]
        ))
        st.metric("Delivery Fee", money(bill["delivery"]))
        st.metric("Final Total", money(bill["total"]))

        if cart:
            receipt_rows = []

            for name, quantity in cart.items():
                item = PRODUCTS[name]

                receipt_rows.append({
                    "Product": name,
                    "Company": item["company"],
                    "Description": item["generic"],
                    "Quantity": quantity,
                    "Unit Price": item["price"],
                    "Amount": item["price"] * quantity,
                })

            receipt_rows.extend([
                {
                    "Product": "Subtotal",
                    "Company": "",
                    "Description": "",
                    "Quantity": "",
                    "Unit Price": "",
                    "Amount": bill["subtotal"],
                },
                {
                    "Product": "Discount",
                    "Company": "",
                    "Description": discount_choice,
                    "Quantity": "",
                    "Unit Price": "",
                    "Amount": -bill["discount"],
                },
                {
                    "Product": "Membership Benefit",
                    "Company": "",
                    "Description": "",
                    "Quantity": "",
                    "Unit Price": "",
                    "Amount": -bill["membership"],
                },
                {
                    "Product": "Illustrative Tax",
                    "Company": "",
                    "Description": tax_choice,
                    "Quantity": "",
                    "Unit Price": "",
                    "Amount": bill["tax"],
                },
                {
                    "Product": "Delivery",
                    "Company": "",
                    "Description": delivery_method,
                    "Quantity": "",
                    "Unit Price": "",
                    "Amount": bill["delivery"],
                },
                {
                    "Product": "FINAL TOTAL",
                    "Company": "",
                    "Description": "",
                    "Quantity": "",
                    "Unit Price": "",
                    "Amount": bill["total"],
                },
            ])

            csv_content = pd.DataFrame(receipt_rows).to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "Download Itemised Receipt (CSV)",
                data=csv_content,
                file_name=(
                    f"medibill_{st.session_state['invoice_no']}.csv"
                ),
                mime="text/csv",
                use_container_width=True
            )

        else:
            st.info(
                "Your cart is empty. Add a product to generate an itemised receipt."
            )

        st.button(
            "Clear Cart",
            on_click=clear_cart,
            use_container_width=True
        )


# ============================================================
# TAB 2: CONVENIENCE BUNDLES
# ============================================================

with bundles_tab:
    st.subheader("Convenience Bundles")

    st.write(
        "Predefined product groups for demonstration. "
        "These are not medical recommendations."
    )

    bundle_images = {
        "First-Aid Basics": "first_aid_bandage.png",
        "Hydration Supplies": "ors_packet.png",
        "Home Monitoring": "digital_thermometer.png",
        "Everyday Personal Care": "petroleum_jelly.png",
    }

    bundle_columns = st.columns(2)

    for index, (bundle_name, bundle_items) in enumerate(BUNDLES.items()):
        with bundle_columns[index % 2]:
            with st.container(border=True):

                image = asset_path(bundle_images.get(bundle_name))

                if image:
                    st.image(image, use_container_width=True)

                st.markdown(f"### {bundle_name}")

                bundle_total = sum(
                    PRODUCTS[name]["price"] * quantity
                    for name, quantity in bundle_items.items()
                )

                discounted_total = bundle_total * 0.95

                st.markdown(
                    f"**Sample bundle total: {money(discounted_total)}**"
                )

                st.caption(
                    f"Illustrative 5% bundle discount. "
                    f"Original total: {money(bundle_total)}"
                )

                for name, quantity in bundle_items.items():
                    st.write(f"- {name} × {quantity}")

                st.button(
                    "Add Bundle to Cart",
                    key="add_bundle_" + bundle_name,
                    on_click=add_bundle_to_cart,
                    args=(bundle_items,),
                    use_container_width=True
                )


# ============================================================
# TAB 3: SAMPLE PRICE COMPARISON
# ============================================================

with compare_tab:
    st.subheader("Basket Price Comparison")

    st.warning(
        "These provider prices are illustrative estimates, not live prices."
    )

    selected_products = st.multiselect(
        "Choose products to compare",
        list(PRODUCTS.keys()),
        default=["Dolo 650", "Electral", "Band-Aid"]
    )

    if selected_products:
        comparison_rows = []

        for name in selected_products:
            item = PRODUCTS[name]

            row = {
                "Product": name,
                "Company": item["company"],
            }

            for provider, multiplier in PROVIDERS.items():
                row[provider] = round(item["price"] * multiplier, 2)

            comparison_rows.append(row)

        comparison_df = pd.DataFrame(comparison_rows)

        st.dataframe(
            comparison_df,
            hide_index=True,
            use_container_width=True
        )

        provider_totals = {
            provider: sum(
                round(PRODUCTS[name]["price"] * multiplier, 2)
                for name in selected_products
            )
            for provider, multiplier in PROVIDERS.items()
        }

        st.markdown("### Estimated Basket Totals")

        metrics = st.columns(len(provider_totals))

        for index, (provider, total) in enumerate(provider_totals.items()):
            with metrics[index]:
                st.metric(provider, money(total))

        cheapest_provider = min(provider_totals, key=provider_totals.get)

        st.success(
            f"Lowest illustrative basket: {cheapest_provider} "
            f"({money(provider_totals[cheapest_provider])})"
        )

    st.caption(
        "Real price comparison requires verified matching brands, "
        "strengths, pack sizes, sellers, discounts and delivery fees."
    )

    provider_columns = st.columns(3)

    external_providers = [
        ("Tata 1mg", "https://www.1mg.com/"),
        ("PharmEasy", "https://pharmeasy.in/"),
        ("Apollo 24|7", "https://www.apollo247.com/"),
    ]

    for index, (name, url) in enumerate(external_providers):
        with provider_columns[index]:
            st.link_button(
                "Open " + name,
                url,
                use_container_width=True
            )


# ============================================================
# TAB 4: NEARBY PHARMACY SEARCH
# ============================================================

with pharmacy_tab:
    st.subheader("Find Nearby Pharmacies")

    map_location = st.text_input(
        "Enter your area or PIN code",
        placeholder="e.g. Sonipat or 131001",
        key="pharmacy_map_location"
    )

    st.write(
        "MediBill opens a Google Maps search for your chosen area. "
        "It does not access GPS or verify pharmacy stock, opening hours "
        "or distance."
    )

    st.link_button(
        "Search Pharmacies on Google Maps",
        create_maps_url(map_location),
        use_container_width=True
    )

    st.markdown("### Online Pharmacy Websites")

    st.markdown("[Tata 1mg](https://www.1mg.com/)")
    st.markdown("[PharmEasy](https://pharmeasy.in/)")
    st.markdown("[Apollo 24|7](https://www.apollo247.com/)")


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    f"MediBill academic demonstration · {len(PRODUCTS)} catalogue entries · "
    f"{len(BUNDLES)} sample bundles. "
    "Prices and provider comparisons are illustrative. "
    "This application does not process payments, verify live stock, "
    "or provide medical advice. It is not a real tax invoice."
)
