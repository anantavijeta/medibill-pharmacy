
# Dictionary: stores medicine prices
medicine_catalogue = {
    "Paracetamol 500 mg": 30.00,
    "Cetirizine 10 mg": 45.00,
    "ORS Sachets": 25.00,
    "Vitamin C Tablets": 80.00,
    "Antacid Tablets": 55.00,
    "Bandage Pack": 40.00,
    "Digital Thermometer": 150.00
}


# Function: calculates the pharmacy bill
def calculate_bill(items, discount_rate, delivery, membership):

    # Float: stores money values
    subtotal = 0.0

    # Loop: calculate the total for every selected item
    for item in items:
        price = float(item["Unit Price (₹)"])
        quantity = int(item["Quantity"])
        item_total = price * quantity
        subtotal = subtotal + item_total

    # If-elif-else: determine the discount
    if discount_rate == 0.10:
        discount = subtotal * 0.10
    elif discount_rate == 0.05:
        discount = subtotal * 0.05
    else:
        discount = 0.0

    # If-else: calculate membership benefit
    if membership == True:
        membership_benefit = 10.0
    else:
        membership_benefit = 0.0

    # Prevent discounts from exceeding the subtotal
    remaining_amount = subtotal - discount

    if membership_benefit > remaining_amount:
        membership_benefit = remaining_amount

    # If-else: calculate delivery charges
    if delivery == True:
        delivery_fee = 30.0
    else:
        delivery_fee = 0.0

    # Calculate final bill
    total = (
        subtotal
        - discount
        - membership_benefit
        + delivery_fee
    )

    # Return the calculated values in a dictionary
    bill = {
        "subtotal": subtotal,
        "discount": discount,
        "membership_benefit": membership_benefit,
        "delivery_fee": delivery_fee,
        "total": max(0.0, total)
    }

    return bill



