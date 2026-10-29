import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote_plus
import html

st.set_page_config(page_title="MediBill | Pharmacy Billing", layout="wide")

NAVY, BLUE, TEAL = "#17324D", "#2563EB", "#0F766E"
BORDER, INK, MUTED = "#D7DEE7", "#20262E", "#64748B"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {{font-family:Inter,sans-serif;}}
.stApp {{background:#F4F6F9;color:{INK};}}
[data-testid="stSidebar"] {{background:#EEF2F6;border-right:1px solid {BORDER};}}
.hero {{background:linear-gradient(115deg,{NAVY},#244C72 65%,{TEAL});padding:1.3rem 1.5rem;border-radius:15px;color:white;margin-bottom:1rem;}}
.hero h1 {{color:white;margin:0;font-size:2.1rem;}}
.hero p {{color:#E2E8F0;margin:.25rem 0 0 0;}}
div[data-testid="stMetric"] {{background:white;border:1px solid {BORDER};padding:.75rem 1rem;border-radius:10px;}}
div.stButton>button,div.stDownloadButton>button {{border-radius:8px;font-weight:600;}}
.paper-bill {{background:#fffdf2;color:#292820;border:1px solid #c9c4aa;padding:18px;font-family:'Courier New',monospace;box-shadow:0 3px 12px #00000012;}}
.paper-title {{text-align:center;font-weight:bold;font-size:19px;letter-spacing:2px;}}
.paper-subtitle {{text-align:center;font-size:10px;margin:3px 0;}}
.paper-line {{border-top:1px dashed #77745f;margin:9px 0;}}
.paper-meta {{display:flex;justify-content:space-between;gap:8px;font-size:10px;}}
.paper-bill table {{width:100%;border-collapse:collapse;font-family:'Courier New',monospace;font-size:10px;margin-top:8px;}}
.paper-bill th {{border-top:1px solid #6e6b5c;border-bottom:1px solid #6e6b5c;text-align:left;padding:5px 2px;}}
.paper-bill td {{padding:5px 2px;vertical-align:top;border-bottom:1px dotted #c9c4aa;}}
.paper-bill .num {{text-align:right;white-space:nowrap;}}
.paper-total {{text-align:right;font-weight:bold;font-size:14px;margin-top:8px;}}
</style>
<div class="hero"><h1>MediBill</h1><p>Pharmacy catalogue, live billing, basket comparison and a classic paper-style receipt.</p></div>
""", unsafe_allow_html=True)

# Educational catalogue with 56 products across multiple manufacturers.
# Names and prices are examples for a classroom prototype, not verified current retail listings.
DATA = [
("Dolo 650","Paracetamol 650 mg","Micro Labs","Pain relief",32),
("Calpol 500","Paracetamol 500 mg","GSK","Pain relief",24),
("Crocin Advance","Paracetamol 500 mg","Haleon","Pain relief",28),
("Combiflam","Ibuprofen + Paracetamol","Sanofi","Pain relief",42),
("Ibugesic","Ibuprofen","Cipla","Pain relief",38),
("Moov Spray","Topical pain relief","Reckitt","Topical care",145),
("Volini Gel","Topical pain relief","Sun Pharma","Topical care",110),
("Cetirizine","Cetirizine 10 mg","Cipla","Allergy care",22),
("Okacet","Cetirizine 10 mg","Cipla","Allergy care",26),
("Allegra 120","Fexofenadine 120 mg","Sanofi","Allergy care",165),
("Montair LC","Montelukast + Levocetirizine","Cipla","Allergy care",190),
("Sinarest","Cold symptom combination","Centaur","Cold care",45),
("Vicks Action 500","Cold symptom combination","P&G","Cold care",48),
("Strepsils","Throat lozenges","Reckitt","Throat care",45),
("Honitus","Cough syrup","Dabur","Cough care",115),
("Benadryl Cough Formula","Cough syrup","Kenvue","Cough care",125),
("Ascoril LS","Cough syrup","Glenmark","Cough care",130),
("Digene","Antacid tablets","Abbott","Digestive care",32),
("Gelusil","Antacid tablets","Pfizer","Digestive care",40),
("ENO","Antacid powder","Haleon","Digestive care",12),
("Pudin Hara","Digestive care","Dabur","Digestive care",38),
("Electral","ORS sachets","FDC","Hydration",22),
("ORSL","Rehydration drink","Dabur","Hydration",35),
("Enerzal","Electrolyte drink","FDC","Hydration",32),
("Limcee","Vitamin C tablets","Abbott","Vitamins",35),
("Celin 500","Vitamin C tablets","GSK","Vitamins",40),
("Zincovit","Multivitamin supplement","Apex Laboratories","Vitamins",105),
("Supradyn","Multivitamin supplement","Bayer","Vitamins",55),
("Shelcal 500","Calcium supplement","Torrent Pharma","Vitamins",125),
("Neurobion Forte","Vitamin supplement","P&G Health","Vitamins",42),
("Evion 400","Vitamin E supplement","Procter & Gamble","Vitamins",38),
("Becosules","Vitamin supplement","Pfizer","Vitamins",45),
("ORS Powder","Oral rehydration salts","Demo generic brand","Hydration",18),
("Betadine Ointment","Antiseptic ointment","Win-Medicare","First aid",80),
("Savlon Antiseptic","Antiseptic liquid","ITC","First aid",95),
("Dettol Antiseptic","Antiseptic liquid","Reckitt","First aid",90),
("Band-Aid","Adhesive bandages","Kenvue","First aid",45),
("Hansaplast","Adhesive bandages","Beiersdorf","First aid",50),
("Cotton Roll","Medical cotton","Romsons","First aid",38),
("Sterile Gauze","Gauze dressing pack","Dispovan","First aid",55),
("Crepe Bandage","Elastic bandage","Vissco","First aid",95),
("Digital Thermometer","Digital thermometer","Dr Trust","Devices",250),
("BP Monitor","Digital BP monitor","Omron","Devices",1650),
("Pulse Oximeter","Finger pulse oximeter","BPL","Devices",950),
("Glucometer Strips","Test strips pack","Accu-Chek / Roche","Devices",650),
("Sugar Free Gold","Tabletop sweetener","Zydus Wellness","Wellness",95),
("Vaseline Petroleum Jelly","Skin protectant","Unilever","Personal care",65),
("Boroline","Skin cream","G.D. Pharmaceuticals","Personal care",48),
("Nivea Creme","Moisturising cream","Beiersdorf","Personal care",85),
("Septilin","Herbal wellness product","Himalaya Wellness","Wellness",120),
("Aloe Vera Gel","Aloe vera gel","Patanjali","Personal care",90),
("Johnson's Baby Powder","Baby care powder","Kenvue","Baby care",110),
("Pampers Diapers","Baby diaper pack","P&G","Baby care",299),
("Johnson's Baby Lotion","Baby lotion","Kenvue","Baby care",145),
("Otrivin Adult","Nasal spray","Haleon","Nasal care",95),
("Nasivion Adult","Nasal drops","Procter & Gamble","Nasal care",85),
]
PRODUCTS = {r[0]: {"generic":r[1], "company":r[2], "category":r[3], "price":float(r[4])} for r in DATA}

# Sample comparison multipliers demonstrate the interface; these are not live provider prices.
PROVIDERS = {"MediBill demo catalogue":1.00,"Tata 1mg sample estimate":1.04,
             "PharmEasy sample estimate":0.97,"Apollo 24|7 sample estimate":1.02}
DELIVERY = {"Standard delivery (2–4 hours)":25.0,"Express delivery (within 90 minutes)":60.0,
            "Scheduled delivery":20.0,"Store pickup":0.0}
BUNDLES = {
    "First-Aid Basics":{"Band-Aid":1,"Sterile Gauze":1,"Betadine Ointment":1},
    "Hydration Supplies":{"Electral":2,"ORSL":1},
    "Home Monitoring":{"Digital Thermometer":1,"Pulse Oximeter":1},
    "Everyday Personal Care":{"Vaseline Petroleum Jelly":1,"Nivea Creme":1},
}

def money(value):
    return f"₹{value:,.2f}"

def calculate_bill(cart, discount_rate, delivery_fee, membership, tax_rate):
    subtotal = sum(PRODUCTS[n]["price"] * q for n,q in cart.items())
    discount = subtotal * discount_rate
    after_discount = max(0.0, subtotal - discount)
    membership_discount = min(10.0, after_discount) if membership else 0.0
    taxable = max(0.0, after_discount - membership_discount)
    tax = taxable * tax_rate
    return {"subtotal":subtotal,"discount":discount,"membership":membership_discount,
            "taxable":taxable,"tax":tax,"delivery":delivery_fee,
            "total":taxable + tax + delivery_fee}

def maps_url(location):
    query = f"pharmacies near {location}" if location.strip() else "pharmacies near me"
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(query)

def add_bundle(items):
    for name, qty in items.items():
        key = "qty_" + name
        st.session_state[key] = min(100, int(st.session_state.get(key, 0)) + qty)

def receipt_html(cart, bill, discount_label, delivery_label, invoice):
    now = datetime.now().strftime("%d-%m-%Y %H:%M")
    rows = ""
    for name, qty in cart.items():
        item = PRODUCTS[name]
        rows += (f"<tr><td>{html.escape(name)}<br><small>{html.escape(item['company'])}</small></td>"
                 f"<td class='num'>{qty}</td><td class='num'>{item['price']:.2f}</td>"
                 f"<td class='num'>{item['price']*qty:.2f}</td></tr>")
    if not rows:
        rows = "<tr><td colspan='4' style='text-align:center;padding:18px'>No items added</td></tr>"
    return f"""
    <div class="paper-bill">
      <div class="paper-title">MEDIBILL PHARMACY</div>
      <div class="paper-subtitle">SAMPLE BILLING COUNTER</div>
      <div class="paper-subtitle">Educational demonstration • Not a tax invoice</div>
      <div class="paper-line"></div>
      <div class="paper-meta"><span>Invoice: {html.escape(invoice)}</span><span>{now}</span></div>
      <div class="paper-meta"><span>Customer: Walk-in customer</span><span>Copy: Original</span></div>
      <div class="paper-line"></div>
      <table><thead><tr><th>Item / Company</th><th class="num">Qty</th><th class="num">Rate</th><th class="num">Amount</th></tr></thead>
      <tbody>{rows}</tbody></table>
      <div class="paper-line"></div>
      <div class="paper-meta"><span>Subtotal</span><span>{bill['subtotal']:.2f}</span></div>
      <div class="paper-meta"><span>Discount ({html.escape(discount_label)})</span><span>-{bill['discount']:.2f}</span></div>
      <div class="paper-meta"><span>Membership benefit</span><span>-{bill['membership']:.2f}</span></div>
      <div class="paper-meta"><span>Illustrative tax</span><span>{bill['tax']:.2f}</span></div>
      <div class="paper-meta"><span>Delivery: {html.escape(delivery_label)}</span><span>{bill['delivery']:.2f}</span></div>
      <div class="paper-line"></div><div class="paper-total">TOTAL: ₹{bill['total']:.2f}</div>
      <div class="paper-line"></div>
      <div style="font-size:10px">Payment status: Not collected</div>
      <div style="font-size:10px">No live stock, batch, expiry or tax-registration data is connected.</div>
      <div style="font-size:10px;text-align:center;margin-top:12px">Thank you for using MediBill.</div>
    </div>
    """

for product in PRODUCTS:
    st.session_state.setdefault("qty_" + product, 0)
st.session_state.setdefault("invoice_no", "MB" + datetime.now().strftime("%y%m%d%H%M"))

with st.sidebar:
    st.markdown("### Order settings")
    discount_choice = st.selectbox("Discount", ["No discount","5% off","10% off"])
    discount_rate = {"No discount":0.0,"5% off":0.05,"10% off":0.10}[discount_choice]
    membership = st.checkbox("Membership benefit (₹10 off)")
    delivery_method = st.selectbox("Delivery method", list(DELIVERY))
    delivery_fee = DELIVERY[delivery_method]
    st.caption("Sample delivery fee: " + money(delivery_fee))
    tax_choice = st.selectbox("Illustrative tax setting", ["No tax","5% demo tax","12% demo tax"])
    tax_rate = {"No tax":0.0,"5% demo tax":0.05,"12% demo tax":0.12}[tax_choice]
    st.caption("Tax settings are for demonstrating arithmetic only.")
    st.markdown("---")
    location = st.text_input("Area or PIN code", placeholder="e.g., Sonipat or 131001")
    st.link_button("Find nearby pharmacies", maps_url(location), use_container_width=True)

shop_tab, bundles_tab, compare_tab, pharmacy_tab = st.tabs(
    ["Products & paper bill","Bundles","Price comparison","Nearby pharmacies"])

with shop_tab:
    product_col, receipt_col = st.columns([1.4,1], gap="large")
    with product_col:
        st.subheader("Product catalogue")
        search = st.text_input("Search by brand, ingredient or company", placeholder="e.g., Dolo, Cipla, vitamin")
        categories = ["All categories"] + sorted({p["category"] for p in PRODUCTS.values()})
        category = st.selectbox("Filter category", categories)
        shown = [n for n,p in PRODUCTS.items()
                 if (search.lower() in n.lower() or search.lower() in p["generic"].lower() or search.lower() in p["company"].lower())
                 and (category == "All categories" or p["category"] == category)]
        st.caption(f"{len(shown)} products shown · {len(PRODUCTS)} catalogue entries")
        for start in range(0, len(shown), 2):
            cols = st.columns(2)
            for idx, name in enumerate(shown[start:start+2]):
                item = PRODUCTS[name]
                with cols[idx]:
                    with st.container(border=True):
                        st.markdown(f"**{name}**")
                        st.caption(item["generic"])
                        st.markdown(f"<span style='color:{TEAL};font-weight:700'>{money(item['price'])}</span>", unsafe_allow_html=True)
                        st.caption(f"{item['company']} · {item['category']}")
                        st.number_input("Quantity", min_value=0, max_value=100, step=1, key="qty_" + name)
    with receipt_col:
        cart = {n:int(st.session_state["qty_"+n]) for n in PRODUCTS if int(st.session_state["qty_"+n]) > 0}
        bill = calculate_bill(cart, discount_rate, delivery_fee, membership, tax_rate)
        st.subheader("Printed-paper style receipt")
        st.caption("Updates when you change products or order settings.")
        st.markdown(receipt_html(cart,bill,discount_choice,delivery_method,st.session_state.invoice_no), unsafe_allow_html=True)
        if cart:
            rows = [{"Product":n,"Company":PRODUCTS[n]["company"],"Description":PRODUCTS[n]["generic"],
                     "Quantity":q,"Unit price":PRODUCTS[n]["price"],"Amount":PRODUCTS[n]["price"]*q}
                    for n,q in cart.items()]
            rows += [
                {"Product":"Subtotal","Company":"","Description":"","Quantity":"","Unit price":"","Amount":bill["subtotal"]},
                {"Product":"Discount","Company":"","Description":discount_choice,"Quantity":"","Unit price":"","Amount":-bill["discount"]},
                {"Product":"Membership benefit","Company":"","Description":"","Quantity":"","Unit price":"","Amount":-bill["membership"]},
                {"Product":"Illustrative tax","Company":"","Description":tax_choice,"Quantity":"","Unit price":"","Amount":bill["tax"]},
                {"Product":"Delivery","Company":"","Description":delivery_method,"Quantity":"","Unit price":"","Amount":bill["delivery"]},
                {"Product":"TOTAL","Company":"","Description":"","Quantity":"","Unit price":"","Amount":bill["total"]},
            ]
            st.download_button("Download itemised receipt (CSV)", pd.DataFrame(rows).to_csv(index=False).encode("utf-8"),
                file_name=f"medibill_{st.session_state.invoice_no}.csv", mime="text/csv", use_container_width=True)
        if st.button("Clear cart", use_container_width=True):
            for name in PRODUCTS:
                st.session_state["qty_"+name] = 0
            st.session_state.invoice_no = "MB" + datetime.now().strftime("%y%m%d%H%M")
            st.rerun()

with bundles_tab:
    st.subheader("Convenience bundles")
    st.write("Example groupings only. They are not medical recommendations or derived from real purchase history.")
    cols = st.columns(2)
    for i,(bundle_name,items) in enumerate(BUNDLES.items()):
        with cols[i%2]:
            with st.container(border=True):
                st.markdown(f"#### {bundle_name}")
                total = sum(PRODUCTS[n]["price"]*q for n,q in items.items())
                st.markdown(f"**Sample bundle total: {money(total*0.95)}**")
                st.caption("Includes an illustrative 5% bundle discount.")
                for name,qty in items.items():
                    st.write(f"- {name} × {qty}")
                if st.button("Add bundle to cart", key="bundle_"+bundle_name, use_container_width=True):
                    add_bundle(items)
                    st.success("Items added. Return to Products & paper bill to review.")
    st.info("A genuine frequently-bought-together feature would require anonymised transaction data. This prototype uses predefined bundles.")

with compare_tab:
    st.subheader("Compare estimated basket prices")
    st.warning("Provider prices are sample estimates derived from MediBill catalogue prices. They are not live or verified quotes.")
    selected = st.multiselect("Select products to compare", list(PRODUCTS),
                              default=["Dolo 650","Electral","Band-Aid"])
    if selected:
        rows = []
        for name in selected:
            p = PRODUCTS[name]
            row = {"Product":name,"Company":p["company"]}
            for provider,multiplier in PROVIDERS.items():
                row[provider] = round(p["price"]*multiplier,2)
            row["Lowest sample price"] = min(round(p["price"]*m,2) for m in PROVIDERS.values())
            rows.append(row)
        df = pd.DataFrame(rows)
        st.dataframe(df.style.format({c:"₹{:.2f}" for c in df.columns if c not in ("Product","Company")}),
                     hide_index=True, use_container_width=True)
        totals = {provider:sum(round(PRODUCTS[n]["price"]*mult,2) for n in selected)
                  for provider,mult in PROVIDERS.items()}
        st.markdown("#### Basket total by provider")
        cols = st.columns(len(totals))
        for i,(provider,total) in enumerate(totals.items()):
            with cols[i]:
                st.metric(provider,money(total))
        cheapest = min(totals,key=totals.get)
        st.success(f"Lowest sample basket: {cheapest} · {money(totals[cheapest])}")
    st.caption("For a fair comparison, verify exact brand, strength, pack size, seller, availability, discounts, delivery fee and date.")
    cols = st.columns(3)
    for i,(label,url) in enumerate([("Tata 1mg","https://www.1mg.com/"),("PharmEasy","https://pharmeasy.in/"),("Apollo 24|7","https://www.apollo247.com/")]):
        with cols[i]:
            st.link_button("Open "+label,url,use_container_width=True)

with pharmacy_tab:
    st.subheader("Nearby pharmacies")
    search_location = st.text_input("Area or PIN code", value=location, key="map_location")
    st.write("Opens a Google Maps search. MediBill does not read GPS or verify opening hours, stock or distance.")
    st.link_button("Search pharmacies on Google Maps", maps_url(search_location), use_container_width=True)
    st.markdown("#### Online pharmacy websites")
    st.markdown("- [Tata 1mg](https://www.1mg.com/)")
    st.markdown("- [PharmEasy](https://pharmeasy.in/)")
    st.markdown("- [Apollo 24|7](https://www.apollo247.com/)")

st.markdown("---")
st.caption(f"Demo catalogue: {len(PRODUCTS)} entries across multiple companies. All catalogue prices, tax settings, bundles and provider estimates are illustrative. This is not a real tax invoice, does not process payments, and does not provide medical advice. Confirm product suitability and current information with a licensed pharmacist or provider.")
