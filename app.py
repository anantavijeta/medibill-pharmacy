
import streamlit as st
import pandas as pd
from io import StringIO

# 1. Configure the browser tab and layout
st.set_page_config(
    page_title="MediBill | Pharmacy Billing",
    page_icon="💊",
    layout="wide"
)

# 2. Add custom CSS for a clean pharmacy-inspired interface
st.markdown("""
<style>
.stApp {
    background-color: #F7FAF8;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #155C43;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #DCE9E1;
    padding: 16px;
    border-radius: 12px;
}
.stButton button {
    border-radius: 8px;
    font-weight: 600;
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

# 5. Display the website heading
st.title("💊 MediBill")
st.caption("SMART PHARMACY BILLING | Simple • Transparent • Convenient")

st.info(
    "Create an estimated medicine bill, apply eligible discounts "
    "and review the final amount before checkout."
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





