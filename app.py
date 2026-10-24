    "Quantity (packs or units)",
    min_value=1,
    max_value=100,
    value=1,
    step=1,
)

discount_option = st.selectbox(
    "Choose a discount",
    ["No Discount", "5% Discount", "10% Discount"],
)

delivery = st.checkbox("Add delivery service (₹30)")
membership = st.checkbox("Apply eligible member benefit (₹10 off)")
add_second = st.checkbox("Add a second medicine")

second_medicine = None
second_quantity = 1

if add_second:
    second_medicine = st.selectbox(
        "Choose your second medicine",
        list(medicine_prices.keys()),
        key="second_medicine",
    )
    second_quantity = st.number_input(
        "Quantity of second medicine",
        min_value=1,
        max_value=100,
        value=1,
        step=1,
        key="second_quantity",
    )

# ---------------------------------------------------------
# Bill calculations
# ---------------------------------------------------------
subtotal = medicine_prices[medicine] * quantity

if add_second and second_medicine is not None:
    subtotal += medicine_prices[second_medicine] * second_quantity

if discount_option == "5% Discount":
    discount_rate = 0.05
elif discount_option == "10% Discount":
    discount_rate = 0.10
else:
    discount_rate = 0.0

discount_amount = subtotal * discount_rate
delivery_fee = 30.0 if delivery else 0.0
membership_discount = 10.0 if membership else 0.0

# Do not let the membership benefit reduce the medicine total below zero.
membership_discount = min(
    membership_discount,
    max(0.0, subtotal - discount_amount),
)

final_total = (
    subtotal
    - discount_amount
    - membership_discount
    + delivery_fee
)

# ---------------------------------------------------------
# Bill summary
# ---------------------------------------------------------
st.divider()
st.header("2. Your Bill Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Subtotal", f"₹{subtotal:,.2f}")
col2.metric(
    "Total Savings",
    f"₹{discount_amount + membership_discount:,.2f}",
)
col3.metric("Final Amount", f"₹{final_total:,.2f}")

with st.expander("View bill breakdown", expanded=True):
    st.write(f"**Selected medicine:** {medicine}")
    st.write(f"**Quantity:** {quantity}")
    st.write(f"**Unit price:** ₹{medicine_prices[medicine]:,.2f}")

    if add_second and second_medicine is not None:
        st.write(f"**Second medicine:** {second_medicine}")
        st.write(f"**Second quantity:** {second_quantity}")
        st.write(
            "**Second medicine unit price:** "
            f"₹{medicine_prices[second_medicine]:,.2f}"
        )

    st.write(f"**Subtotal:** ₹{subtotal:,.2f}")
    st.write(f"**Discount:** −₹{discount_amount:,.2f}")
    st.write(f"**Membership benefit:** −₹{membership_discount:,.2f}")
    st.write(f"**Delivery fee:** ₹{delivery_fee:,.2f}")

st.divider()
st.success(f"Amount Payable: ₹{final_total:,.2f}")

st.caption(
    "Note: Listed medicine prices are illustrative estimates, not verified "
    "market prices. Confirm actual prices with your pharmacy."
)

st.markdown(
    """
    <div class="medi-footer">
        <span class="medi-doodle">✿</span>
        &nbsp; MediBill · Thoughtful design, transparent billing
        &nbsp; <span class="medi-doodle">✳</span>
    </div>
    """,
    unsafe_allow_html=True,
)


