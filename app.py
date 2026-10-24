
import streamlit as st

# MediBill: Pharmacy Medicine Bill Calculator

# Configure the browser tab and page layout
st.set_page_config(
    page_title="MediBill | Pharmacy Calculator",
    page_icon="💊",
    layout="centered"
)

# MediBill visual theme: sage, royal blue and pink
st.markdown("""
<style>
/* Main page background and typography */
.stApp {
    background-color: #F8F8F2;
    color: #294634;
}

/* Keep the main content comfortable and spacious */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1050px;
}

/* Headings */
h1, h2, h3 {
    color: #294634 !important;
}

/* Buttons */
.stButton > button {
    background-color: #3655B3;
    color: #FFFFFF;
    border: 1px solid #3655B3;
    border-radius: 12px;
    padding: 0.55rem 1rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #29438F;
    border-color: #29438F;
    color: #FFFFFF;
}

/* Input fields */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: #FFFFFF;
    border-color: #D5E1D0;
    border-radius: 10px;
}

/* Checkboxes */
.stCheckbox label {
    color: #355640;
}

/* Subtle dividers */
hr {
    border-color: #DCE8D5;
}

/* Result metric cards */
div[data-testid="stMetric"] {
    background-color: #E8EFE2;
    border: 1px solid #D4E2CF;
    padding: 16px;
    border-radius: 14px;
}

/* Pink success and info accents */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Expander cards */
div[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE8D5;
    border-radius: 12px;
}

/* Small footer text */
.medi-footer {
    color: #66806A;
    text-align: center;
    font-size: 0.85rem;
    padding: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Display the website title and introduction
st.title("💊 MediBill")

# Custom MediBill header with small decorative doodles
st.markdown("""
<div style="
    background: linear-gradient(120deg, #E2EBDD, #F5E5ED);
    padding: 28px;
    border-radius: 20px;
    border: 1px solid #D5E1D0;
    margin-bottom: 24px;
">
    <div style="
        font-size: 14px;
        color: #3655B3;
        letter-spacing: 2px;
        font-weight: 600;
    ">
        ✳ YOUR FRIENDLY PHARMACY CALCULATOR ✳
    </div>

    <h1 style="
        color: #294634;
        font-size: 42px;
        margin: 8px 0 4px 0;
    ">
        💊 MediBill
        <span style="color: #D987A9;">♡</span>
    </h1>

    <p style="
        color: #54745C;
        font-size: 16px;
        margin-bottom: 8px;
    ">
        Simple billing. Clear totals. A little more care.
    </p>

    <div style="
        color: #3655B3;
        font-size: 18px;
        letter-spacing: 8px;
    ">
        ✿  +  ☆  ✿
    </div>
</div>
""", unsafe_allow_html=True)

st.write(
    "Build your order below and see your estimated "
    "medicine bill instantly."
)

st.subheader("Pharmacy Medicine Bill Calculator")
st.write(
    "Calculate your estimated medicine bill quickly "
    "with a clear breakdown of your order."
)

# Store illustrative medicine prices in a dictionary
medicine_prices = {
    "Paracetamol 500 mg": 30.0,
    "Cetirizine 10 mg": 45.0,
    "ORS Sachets": 25.0,
    "Vitamin C Tablets": 80.0,
    "Antacid Tablets": 55.0
}

st.divider()
st.header("1. Create Your Order")

# Input 1: Select the medicine
medicine = st.selectbox(
    "Choose a medicine",
    list(medicine_prices.keys())
)

# Input 2: Enter the quantity
quantity = st.number_input(
    "Quantity (packs or units)",
    min_value=1,
    max_value=100,
    value=1,
    step=1
)

# Input 3: Select the discount option
discount_option = st.selectbox(
    "Choose a discount",
    ["No Discount", "5% Discount", "10% Discount"]
)

# Input 4: Choose delivery
delivery = st.checkbox("Add delivery service (₹30)")

# Input 5: Choose membership
membership = st.checkbox("Apply eligible member benefit (₹10 off)")

# Input 6: Select another medicine
add_second = st.checkbox("Add a second medicine")

second_medicine = None
second_quantity = 1

if add_second:
    second_medicine = st.selectbox(
        "Choose your second medicine",
        list(medicine_prices.keys()),
        key="second_medicine"
    )
    second_quantity = st.number_input(
        "Quantity of second medicine",
        min_value=1,
        max_value=100,
        value=1,
        step=1,
        key="second_quantity"
    )

st.divider()
st.header("2. Your Bill")

# Calculate the first medicine's subtotal
subtotal = medicine_prices[medicine] * quantity

# Add the second medicine only when selected
if add_second and second_medicine is not None:
    subtotal += medicine_prices[second_medicine] * second_quantity

# Apply the discount using conditional statements
if discount_option == "5% Discount":
    discount_rate = 0.05
elif discount_option == "10% Discount":
    discount_rate = 0.10
else:
    discount_rate = 0.0

discount_amount = subtotal * discount_rate

# Calculate optional fees and membership benefit
delivery_fee = 30.0 if delivery else 0.0
membership_discount = 10.0 if membership else 0.0

# Prevent the membership benefit from exceeding the remaining bill
membership_discount = min(
    membership_discount,
    subtotal - discount_amount
)

# Calculate the final estimated amount
final_total = (
    subtotal
    - discount_amount
    - membership_discount
    + delivery_fee
)


# Display a structured bill summary
st.divider()
st.header("3. Your Order Summary")

# Display the main financial figures in separate columns
col1, col2, col3 = st.columns(3)

col1.metric(
    "Subtotal",
    f"₹{subtotal:,.2f}"
)

col2.metric(
    "Total Savings",
    f"₹{discount_amount + membership_discount:,.2f}"
)

col3.metric(
    "Final Amount",
    f"₹{final_total:,.2f}"
)

# Show a detailed breakdown for transparency
with st.expander("View bill breakdown", expanded=True):
    st.write(f"**Selected medicine:** {medicine}")
    st.write(f"**Quantity:** {quantity}")
    st.write(
        f"**Unit price:** ₹{medicine_prices[medicine]:,.2f}"
    )

    if add_second and second_medicine is not None:
        st.write(
            f"**Second medicine:** {second_medicine}"
        )
        st.write(
            f"**Second quantity:** {second_quantity}"
        )

    st.write(f"**Subtotal:** ₹{subtotal:,.2f}")
    st.write(f"**Discount:** −₹{discount_amount:,.2f}")
    st.write(
        f"**Membership benefit:** "
        f"−₹{membership_discount:,.2f}"
    )
    st.write(f"**Delivery fee:** ₹{delivery_fee:,.2f}")

    st.divider()
    st.success(f"Amount Payable: ₹{final_total:,.2f}")
