
import streamlit as st
import pandas as pd
from io import StringIO

# 1. Configure the browser tab and layout
st.set_page_config(
    page_title="MediBill | Pharmacy Billing",
    page_icon="💊",
    layout="wide"
)

# 2. 
# MediBill visual identity: pink, royal blue, sage and peacock green
st.markdown("""
<style>
/* ---------- BRAND COLOURS ---------- */
:root {
    --pink: #F5A6C8;
    --pink-light: #FFF0F6;
    --royal-blue: #4169E1;
    --sage: #B7CBB7;
    --sage-light: #EFF5EF;
    --peacock: #005B50;
    --peacock-dark: #003F38;
    --cream: #FFFAFC;
    --text: #263C37;
}

/* ---------- MAIN WEBSITE BACKGROUND ---------- */
.stApp {
    background-color: var(--cream);
    color: var(--text);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* ---------- HEADINGS ---------- */
h1, h2, h3 {
    color: var(--peacock) !important;
    font-weight: 750 !important;
    letter-spacing: -0.5px;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #EFF5EF 0%,
        #FCEAF2 100%
    );
    border-right: 2px solid #D9E7DC;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--peacock) !important;
}

/* ---------- METRIC CARDS ---------- */
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #D7E5DA;
    border-top: 4px solid var(--pink);
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0, 91, 80, 0.06);
}

div[data-testid="stMetricLabel"] {
    color: var(--peacock) !important;
}

div[data-testid="stMetricValue"] {
    color: var(--royal-blue) !important;
    font-weight: 750;
}

/* ---------- BUTTONS ---------- */
.stButton button,
.stDownloadButton button {
    background: var(--peacock);
    color: white;
    border: 2px solid var(--peacock);
    border-radius: 12px;
    padding: 0.55rem 1rem;
    font-weight: 650;
    transition: all 0.2s ease;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background: var(--royal-blue);
    border-color: var(--royal-blue);
    color: white;
}

/* ---------- INPUT BOXES ---------- */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: white;
    border-radius: 10px;
    border-color: var(--sage);
}

/* ---------- CHECKBOXES AND RADIO BUTTONS ---------- */
div[data-testid="stCheckbox"] label,
div[data-testid="stRadio"] label {
    color: var(--peacock-dark);
}

/* ---------- CONTAINERS AND PRODUCT CARDS ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #D8E5DB;
    border-radius: 16px;
}

/* ---------- INFO, SUCCESS AND WARNING BOXES ---------- */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* ---------- TABLE ---------- */
div[data-testid="stDataFrame"] {
    border: 1px solid #D8E5DB;
    border-radius: 12px;
    overflow: hidden;
}

/* ---------- MEDICINE DOODLE HEADER ---------- */
.medibill-header {
    position: relative;
    overflow: hidden;
    background: linear-gradient(
        125deg,
        #FFF0F6 0%,
        #EFF5EF 55%,
        #E8EEFF 100%
    );
    border: 1px solid #E6DCE8;
    border-radius: 24px;
    padding: 30px;
    margin-bottom: 22px;
}

.medibill-brand {
    color: #005B50;
    font-size: 2.65rem;
    font-weight: 850;
    letter-spacing: -1.5px;
    line-height: 1.2;
}

.medibill-tagline {
    color: #4169E1;
    font-size: 1rem;
    margin-top: 8px;
    font-weight: 550;
}

.medibill-doodle {
    font-size: 1.8rem;
    letter-spacing: 10px;
    margin-top: 14px;
}

.medibill-label {
    display: inline-block;
    background: #F5A6C8;
    color: #4D2340;
    border-radius: 30px;
    padding: 6px 13px;
    font-size: 0.78rem;
    font-weight: 750;
    margin-top: 12px;
}

/* ---------- SECTION LABELS ---------- */
.section-label {
    color: #005B50;
    font-weight: 750;
    font-size: 1.1rem;
    padding-bottom: 8px;
    border-bottom: 2px solid #B7CBB7;
    margin-bottom: 15px;
}

/* ---------- SMALL SCREEN SUPPORT ---------- */
@media (max-width: 640px) {
    .medibill-header {
        padding: 20px;
        border-radius: 18px;
    }

    .medibill-brand {
        font-size: 2rem;
    }

    .medibill-doodle {
        font-size: 1.4rem;
        letter-spacing: 5px;
    }
}
</style>
""", unsafe_allow_html=True)



# 3. Define the illustrative medicine catalogue
medicine_catalogue = {
    "Paracetamol 500 mg": 30.00,
    "Cetirizine 10 mg": 45.00,
    "ORS Sachets": 25.00,
    "Vitamin C Tablets": 80.00,
    "Antacid Tablets": 55.00,
    "Bandage Pack": 40.00,
    "Digital Thermometer": 150.00,
}

# 4. Create a reusable function for calculating the bill
def calculate_bill(items, discount_rate, delivery, membership):
    subtotal = sum(
        item["Unit Price (₹)"] * item["Quantity"]
        for item in items
    )

    # Calculate the selected percentage discount
    discount = subtotal * discount_rate

    # Calculate the membership benefit and cap discounts
    # so the total discounts cannot exceed the subtotal
    membership_benefit = 10.00 if membership else 0.00
    membership_benefit = min(
        membership_benefit,
        max(0.0, subtotal - discount)
    )

    # Apply the optional delivery fee
    delivery_fee = 30.00 if delivery else 0.00

    # Calculate the amount payable
    total = (
        subtotal
        - discount
        - membership_benefit
        + delivery_fee
    )

    return {
        "subtotal": subtotal,
        "discount": discount,
        "membership_benefit": membership_benefit,
        "delivery_fee": delivery_fee,
        "total": max(0.0, total),
    }

# 5. 
# Custom branded header with medicine and tablet doodles
st.markdown("""
<div class="medibill-header">
    <div class="medibill-brand">
        MediBill 💊
    </div>

    <div class="medibill-tagline">
        Your health essentials, clearly priced.
    </div>

    <div class="medibill-doodle">
        💊 🩹 🧴 💗 🩺 💉
    </div>

    <div class="medibill-label">
        SMART PHARMACY BILLING
    </div>
</div>
""", unsafe_allow_html=True)

st.write(
    "Create an estimated medicine bill, apply eligible discounts, "
    "and review your total in one simple place."
)


# 6. Organize the website into a sidebar and main billing area
with st.sidebar:
    st.header("⚙️ Billing Options")

    discount_choice = st.selectbox(
        "Discount tier",
        ["No Discount", "5% Discount", "10% Discount"]
    )

    # Use conditional logic to determine the discount rate
    if discount_choice == "5% Discount":
        discount_rate = 0.05
    elif discount_choice == "10% Discount":
        discount_rate = 0.10
    else:
        discount_rate = 0.0

    delivery = st.checkbox("Add delivery service (+₹30)")
    membership = st.checkbox("Eligible member benefit (₹10 off)")

    st.divider()
    st.caption("Demo catalogue only. Prices are illustrative.")

# 7. Collect the medicine order from the user
st.header("1. Build your order")
st.write("Select up to five different products and enter the required quantities.")

selected_items = []
product_names = list(medicine_catalogue.keys())

# 8. Display product selectors in a two-column layout
for start in range(0, 5, 2):
    columns = st.columns(2)

    for offset, column in enumerate(columns):
        index = start + offset

        if index >= 5:
            continue

        with column:
            with st.container(border=True):
                product = st.selectbox(
                    f"Medicine / Product {index + 1}",
                    ["None"] + product_names,
                    key=f"product_{index}"
                )

                # Quantity input appears only for a selected product
                if product != "None":
                    quantity = st.number_input(
                        f"Quantity for {product}",
                        min_value=1,
                        max_value=100,
                        value=1,
                        step=1,
                        key=f"quantity_{index}"
                    )

                    selected_items.append({
                        "Medicine": product,
                        "Unit Price (₹)": medicine_catalogue[product],
                        "Quantity": int(quantity),
                        "Line Total (₹)": (
                            medicine_catalogue[product] * quantity
                        ),
                    })
                else:
                    st.caption("Choose a product to add it to the bill.")

# 9. Validate the order before performing calculations
st.divider()
st.header("2. Bill Summary")

if not selected_items:
    st.warning("Please select at least one medicine or product to calculate a bill.")
else:
    # 10. Calculate the bill using the reusable function
    bill = calculate_bill(
        selected_items,
        discount_rate,
        delivery,
        membership
    )

    # 11. Display key totals as summary metrics
    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Medicine Subtotal",
        f"₹{bill['subtotal']:,.2f}"
    )
    metric2.metric(
        "Total Discounts",
        f"₹{bill['discount'] + bill['membership_benefit']:,.2f}"
    )
    metric3.metric(
        "Amount Payable",
        f"₹{bill['total']:,.2f}"
    )

    # 12. Display a detailed itemized receipt
    st.subheader("🧾 Itemized Receipt")

    receipt = pd.DataFrame(selected_items)
    st.dataframe(
        receipt,
        use_container_width=True,
        hide_index=True
    )

    # 13. Show the full calculation breakdown
    with st.container(border=True):
        st.write("**Price Breakdown**")
        st.write(f"Medicine subtotal: ₹{bill['subtotal']:,.2f}")
        st.write(f"Percentage discount: −₹{bill['discount']:,.2f}")
        st.write(
            f"Membership benefit: "
            f"−₹{bill['membership_benefit']:,.2f}"
        )
        st.write(f"Delivery charge: ₹{bill['delivery_fee']:,.2f}")

        st.divider()
        st.markdown(
            f"### Estimated Total: ₹{bill['total']:,.2f}"
        )

    # 14. Provide a downloadable receipt in CSV format
    csv_buffer = StringIO()
    receipt.to_csv(csv_buffer, index=False)

    st.download_button(
        label="⬇️ Download Itemized Receipt (CSV)",
        data=csv_buffer.getvalue(),
        file_name="medibill_receipt.csv",
        mime="text/csv"
    )

    st.success("Your estimated bill has been calculated successfully.")

# 15. Add a footer clarifying the purpose and limitations of the app
st.divider()
st.caption(
    "MediBill is an educational billing prototype. Product prices, "
    "discounts and fees are illustrative. It is not a live pharmacy "
    "catalogue, prescription service or medical recommendation system."
)




