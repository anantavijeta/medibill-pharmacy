
import streamlit as st
import pandas as pd
from io import StringIO

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="MediBill | Pharmacy Studio",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. MEDIBILL COLOUR PALETTE
# Pink, Royal Blue, Sage Green and Peacock Dark Green
# ============================================================
PINK = "#F5A6C8"
LIGHT_PINK = "#FFF0F6"
ROYAL_BLUE = "#4169E1"
SAGE_GREEN = "#A8BFA3"
PEACOCK_GREEN = "#064E45"
DARK_GREEN = "#123D35"
CREAM = "#FFFAFC"
WHITE = "#FFFFFF"
TEXT = "#263B37"

# ============================================================
# 3. CUSTOM CSS AND DECORATIVE MEDICINE DOODLES
# ============================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root {{
    --pink: {PINK};
    --light-pink: {LIGHT_PINK};
    --royal-blue: {ROYAL_BLUE};
    --sage: {SAGE_GREEN};
    --peacock: {PEACOCK_GREEN};
    --dark-green: {DARK_GREEN};
    --cream: {CREAM};
    --text: {TEXT};
}}

.stApp {{
    background:
        radial-gradient(ellipse at 4% 12%,
            rgba(245,166,200,0.16), transparent 27%),
        radial-gradient(ellipse at 94% 35%,
            rgba(168,191,163,0.19), transparent 28%),
        {CREAM};
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}}

.block-container {{
    padding-top: 1.7rem;
    padding-bottom: 2.5rem;
    max-width: 1400px;
}}

h1, h2, h3 {{
    color: var(--peacock) !important;
    font-family: 'Playfair Display', Georgia, serif !important;
}}

p, label, span {{
    font-family: 'DM Sans', sans-serif;
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(
        180deg, #FCE5EF 0%, #F4EAFB 48%, #E6F0E5 100%
    );
    border-right: 1px solid #E6C8D8;
}}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    color: var(--peacock) !important;
}}

[data-testid="stMetric"] {{
    background: white;
    border: 1px solid #E5DCE5;
    border-radius: 16px;
    padding: 17px;
    box-shadow: 0 5px 18px rgba(6,78,69,0.05);
}}

[data-testid="stMetricLabel"] {{
    color: var(--peacock) !important;
}}

[data-testid="stMetricValue"] {{
    color: var(--royal-blue) !important;
    font-weight: 700;
}}

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(255,255,255,0.82);
    border: 1px solid #E8DDE7;
    border-radius: 17px;
    padding: 12px;
}}

.stButton > button,
.stDownloadButton > button {{
    background: var(--peacock);
    color: white;
    border: 1px solid var(--peacock);
    border-radius: 12px;
    font-weight: 600;
    min-height: 43px;
    transition: all 0.2s ease;
}}

.stButton > button:hover,
.stDownloadButton > button:hover {{
    background: var(--royal-blue);
    border-color: var(--royal-blue);
    color: white;
}}

div[data-baseweb="select"] > div {{
    border-radius: 10px;
    border-color: #D8C8D8;
}}

input {{
    border-radius: 10px !important;
}}

hr {{
    border-color: #EADCE7;
}}

.medi-hero {{
    position: relative;
    overflow: hidden;
    background: linear-gradient(
        120deg, #064E45 0%, #12695B 56%, #4169E1 120%
    );
    border-radius: 25px;
    padding: 32px 34px;
    margin-bottom: 22px;
    color: white;
    box-shadow: 0 12px 32px rgba(6,78,69,0.15);
}}

.medi-hero h1 {{
    color: white !important;
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: 43px !important;
    margin: 0;
    letter-spacing: -1px;
}}

.medi-hero p {{
    color: #F7EAF3;
    margin: 7px 0 0 0;
    font-size: 14px;
}}

.hero-label {{
    color: #F5A6C8;
    font-size: 10px;
    letter-spacing: 3px;
    font-weight: 700;
    margin-bottom: 8px;
}}

.doodle-cloud {{
    position: absolute;
    right: 24px;
    top: 12px;
    width: 215px;
    height: 135px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 10px;
    transform: rotate(-5deg);
    opacity: 0.96;
}}

.doodle {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.35);
    border-radius: 17px;
    width: 51px;
    height: 51px;
    font-size: 25px;
    transform: rotate(7deg);
}}

.doodle:nth-child(even) {{
    transform: rotate(-12deg);
    background: rgba(245,166,200,0.22);
}}

.section-label {{
    background: linear-gradient(90deg, #FCE4EF, #E8EAFE);
    color: #064E45;
    border-left: 4px solid #4169E1;
    border-radius: 8px;
    padding: 10px 14px;
    font-weight: 700;
    margin: 12px 0 16px 0;
}}

.mini-label {{
    color: #52756A;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}}

.total-banner {{
    background: linear-gradient(115deg, #064E45, #12695B);
    color: white;
    padding: 23px;
    border-radius: 19px;
    margin: 12px 0;
}}

.total-banner .amount {{
    color: #F5A6C8;
    font-size: 35px;
    font-weight: 700;
}}

.total-banner .caption {{
    color: #E3F0E8;
    font-size: 12px;
}}

.medi-footer {{
    background: #F8EAF1;
    border: 1px solid #EBD7E2;
    border-radius: 15px;
    padding: 16px;
    color: #52685F;
    text-align: center;
    font-size: 12px;
}}

@media (max-width: 700px) {{
    .medi-hero {{
        padding: 23px 20px;
    }}
    .medi-hero h1 {{
        font-size: 34px !important;
    }}
    .doodle-cloud {{
        opacity: 0.3;
        right: -40px;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 4. HEADER WITH MEDICINE AND TABLET DOODLES
# ============================================================
st.markdown("""
<div class="medi-hero">
    <div class="hero-label">YOUR FRIENDLY PHARMACY COMPANION</div>
    <h1>♡ MediBill</h1>
    <p>Thoughtful healthcare. Transparent billing. One little app.</p>
    <div class="doodle-cloud">
        <span class="doodle">💊</span>
        <span class="doodle">🩹</span>
        <span class="doodle">🧴</span>
        <span class="doodle">🩺</span>
        <span class="doodle">🌿</span>
        <span class="doodle">🩷</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 5. ILLUSTRATIVE MEDICINE CATALOGUE
# Prices are examples, not verified retail prices.
# ============================================================
medicine_catalogue = {
    "Paracetamol 500 mg": 30.00,
    "Cetirizine 10 mg": 45.00,
    "ORS Sachets": 25.00,
    "Vitamin C Tablets": 80.00,
    "Antacid Tablets": 55.00,
    "Bandage Pack": 40.00,
    "Digital Thermometer": 150.00,
}

# ============================================================
# 6. REUSABLE BILL CALCULATION FUNCTION
# ============================================================
def calculate_bill(items, discount_rate, delivery, membership):
    # Multiply the unit price by quantity for each product
    subtotal = sum(
        item["Unit Price (₹)"] * item["Quantity"]
        for item in items
    )

    # Calculate the selected percentage discount
    discount = subtotal * discount_rate

    # Calculate the fixed membership benefit
    membership_benefit = 10.00 if membership else 0.00

    # Ensure the membership benefit cannot exceed the
    # amount remaining after the percentage discount
    membership_benefit = min(
        membership_benefit,
        max(0.0, subtotal - discount)
    )

    # Apply delivery fees only if the customer selects delivery
    delivery_fee = 30.00 if delivery else 0.00

    # Calculate the amount payable after discounts and fees
    total = (
        subtotal
        - discount
        - membership_benefit
        + delivery_fee
    )

    # Return all amounts together for display and testing
    return {
        "subtotal": subtotal,
        "discount": discount,
        "membership_benefit": membership_benefit,
        "delivery_fee": delivery_fee,
        "total": max(0.0, total),
    }

# ============================================================
# 7. SIDEBAR BILLING SETTINGS
# ============================================================
with st.sidebar:
    st.markdown("## 🌸 Billing Studio")
    st.caption("Personalize your sample order")

    st.markdown("---")

    discount_choice = st.selectbox(
        "🎀 Discount tier",
        ["No Discount", "5% Discount", "10% Discount"]
    )

    # Select the discount rate based on the user's choice
    if discount_choice == "5% Discount":
        discount_rate = 0.05
    elif discount_choice == "10% Discount":
        discount_rate = 0.10
    else:
        discount_rate = 0.0

    st.markdown("### ✨ Extra services")
    delivery = st.checkbox("🚚 Delivery (+₹30)")
    membership = st.checkbox("💗 Member benefit (₹10 off)")

    st.markdown("---")

    st.markdown("### 🎨 Colour palette")
    st.markdown(
        f"""
        <div style="display:flex;gap:6px;flex-wrap:wrap;">
          <div title="Pink" style="background:{PINK};width:30px;height:30px;border-radius:50%;"></div>
          <div title="Royal Blue" style="background:{ROYAL_BLUE};width:30px;height:30px;border-radius:50%;"></div>
          <div title="Sage Green" style="background:{SAGE_GREEN};width:30px;height:30px;border-radius:50%;"></div>
          <div title="Peacock Green" style="background:{PEACOCK_GREEN};width:30px;height:30px;border-radius:50%;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Illustrative catalogue • No live pharmacy data")

# ============================================================
# 8. ORDER INPUTS
# ============================================================
st.markdown(
    '<div class="section-label">01 &nbsp; ✿ &nbsp; BUILD YOUR ORDER</div>',
    unsafe_allow_html=True
)
st.write("Choose your products and quantities below.")

selected_items = []
product_names = list(medicine_catalogue.keys())

# Display five product slots in a two-column layout
for start in range(0, 5, 2):
    columns = st.columns(2)

    for offset, column in enumerate(columns):
        index = start + offset

        if index >= 5:
            continue

        with column:
            with st.container(border=True):
                st.markdown(
                    f'<div class="mini-label">PRODUCT SLOT {index + 1}</div>',
                    unsafe_allow_html=True
                )

                product = st.selectbox(
                    "Medicine or healthcare product",
                    ["None"] + product_names,
                    key=f"product_{index}"
                )

                if product != "None":
                    unit_price = medicine_catalogue[product]

                    st.markdown(
                        f"""
                        <div style="
                            background:#FCEAF2;
                            border-radius:10px;
                            padding:9px 12px;
                            margin:4px 0 12px 0;
                            color:#064E45;
                        ">
                            💊 <b>{product}</b><br>
                            <span style="font-size:12px;">
                                Sample unit price: ₹{unit_price:,.2f}
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    quantity = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=100,
                        value=1,
                        step=1,
                        key=f"quantity_{index}"
                    )

                    selected_items.append({
                        "Medicine": product,
                        "Unit Price (₹)": unit_price,
                        "Quantity": int(quantity),
                        "Line Total (₹)": unit_price * quantity,
                    })
                else:
                    st.caption("Your next product can go here ♡")

# ============================================================
# 9. BILL SUMMARY
# ============================================================
st.markdown(
    '<div class="section-label">02 &nbsp; ✿ &nbsp; YOUR BILL</div>',
    unsafe_allow_html=True
)

if not selected_items:
    st.warning(
        "🌷 Your order is waiting! Choose at least one product "
        "above to calculate your bill."
    )
else:
    # Calculate the order using the reusable function
    bill = calculate_bill(
        selected_items,
        discount_rate,
        delivery,
        membership
    )

    # Display three summary metrics
    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "🧺 Subtotal",
        f"₹{bill['subtotal']:,.2f}"
    )

    metric2.metric(
        "🎀 Total savings",
        f"₹{bill['discount'] + bill['membership_benefit']:,.2f}"
    )

    metric3.metric(
        "💚 Amount payable",
        f"₹{bill['total']:,.2f}"
    )

    st.markdown("### 🧾 Your itemized receipt")

    # Convert the selected products into a table
    receipt = pd.DataFrame(selected_items)

    st.dataframe(
        receipt,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Unit Price (₹)": st.column_config.NumberColumn(
                "Unit Price",
                format="₹%.2f"
            ),
            "Line Total (₹)": st.column_config.NumberColumn(
                "Line Total",
                format="₹%.2f"
            ),
        }
    )

    # Show a separate, detailed price breakdown
    with st.container(border=True):
        st.markdown("#### 🌿 Price breakdown")

        left, right = st.columns([3, 2])

        with left:
            st.write("Medicine subtotal")
            st.write("Percentage discount")
            st.write("Membership benefit")
            st.write("Delivery charge")

        with right:
            st.markdown(
                f"<div style='text-align:right;color:{PEACOCK_GREEN};'>"
                f"₹{bill['subtotal']:,.2f}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='text-align:right;color:{ROYAL_BLUE};'>"
                f"− ₹{bill['discount']:,.2f}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='text-align:right;color:{ROYAL_BLUE};'>"
                f"− ₹{bill['membership_benefit']:,.2f}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='text-align:right;color:{PEACOCK_GREEN};'>"
                f"₹{bill['delivery_fee']:,.2f}</div>",
                unsafe_allow_html=True
            )

        st.markdown(
            f"""
            <div class="total-banner">
                <div class="caption">YOUR ESTIMATED TOTAL</div>
                <div class="amount">₹{bill['total']:,.2f}</div>
                <div class="caption">
                    Thank you for choosing MediBill ♡
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # 10. DOWNLOADABLE RECEIPT
    # ========================================================
    st.markdown("### 📥 Take your receipt with you")

    csv_buffer = StringIO()
    receipt.to_csv(csv_buffer, index=False)

    st.download_button(
        label="♡ Download itemized receipt (CSV)",
        data=csv_buffer.getvalue(),
        file_name="medibill_receipt.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.success("Your estimated bill is ready! 🌸")

# ============================================================
# 11. FOOTER AND EDUCATIONAL DISCLAIMER
# ============================================================
st.markdown("---")

st.markdown("""
<div class="medi-footer">
    <div style="font-size:22px;margin-bottom:5px;">
        💊 🌿 💗
    </div>
    <b style="color:#064E45;">MediBill Pharmacy Studio</b><br>
    Made with care, colour and Python.<br><br>
    Educational billing prototype only. All product prices,
    discounts and service charges are illustrative.
    This application is not a live pharmacy catalogue,
    prescription service or medical recommendation system.
</div>
""", unsafe_allow_html=True)


