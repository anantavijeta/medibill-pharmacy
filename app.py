
import streamlit as st

# MediBill: Pharmacy Medicine Bill Calculator

# Configure the browser tab and page layout
st.set_page_config(
    page_title="MediBill | Pharmacy Calculator",
    page_icon="💊",
    layout="centered"
)

# Display the website title and introduction
st.title("💊 MediBill")
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

# Display the bill breakdown
st.write(f"**Medicine subtotal:** ₹{subtotal:,.2f}")
st.write(f"**Discount:** −₹{discount_amount:,.2f}")
st.write(f"**Membership benefit:** −₹{membership_discount:,.2f}")
st.write(f"**Delivery fee:** ₹{delivery_fee:,.2f}")

st.divider()

# Highlight the final bill amount
st.success(f"Estimated Total: ₹{final_total:,.2f}")

# Explain the limitations of the demonstration
st.caption(
    "Educational demo using illustrative prices. "
    "Not a live pharmacy catalogue or medical recommendation."
)




