import streamlit as st
import pandas as pd
from datetime import datetime
from html import escape
from urllib.parse import quote_plus

# MediBill: educational pharmacy billing prototype. Catalogue prices are illustrative.
st.set_page_config(page_title="MediBill | Pharmacy Billing", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Inter,Arial,sans-serif}
.stApp{background:#F5F7FA;color:#1F2937}
[data-testid="stSidebar"]{background:#EEF2F6;border-right:1px solid #D9E1EA}
.hero{padding:22px 26px;border-radius:14px;color:white;background:linear-gradient(110deg,#18324B,#28577A 68%,#0F766E);margin-bottom:16px}
.hero h1{color:white;margin:0;font-size:32px}.hero p{color:#E6EDF4;margin:5px 0 0}
.paper{background:#FFFDF5;color:#202020;border:1px solid #C8C1AF;box-shadow:0 5px 16px #00000012;padding:16px 14px;font-family:"Courier New",monospace;font-size:11px;line-height:1.4;overflow-x:auto}
.rtitle{text-align:center;font-size:17px;font-weight:bold;letter-spacing:1px}.rcenter{text-align:center;font-size:10px}
.rline{border-top:1px dashed #777;margin:8px 0}
.rtable{width:100%;border-collapse:collapse;font-family:"Courier New",monospace;font-size:10px}
.rtable th,.rtable td{border-bottom:1px dotted #B8B09E;padding:4px 2px;text-align:left;vertical-align:top}
.rtable th:last-child,.rtable td:last-child{text-align:right;white-space:nowrap}
.rtotal{display:flex;justify-content:space-between;font-weight:bold;font-size:14px;margin-top:8px}
div[data-testid="stMetric"]{background:white;border:1px solid #D9E1EA;padding:12px;border-radius:10px}
</style>
<div class="hero"><h1>MediBill</h1><p>Pharmacy billing, sample price comparisons, and a classic paper-style receipt.</p></div>
""", unsafe_allow_html=True)

# Brand, generic/product description, company, sample price, category, pack.
# Verify actual company, pack, price, and availability before using outside this demo.
ROWS = [
("Dolo 650","Paracetamol 650 mg","Micro Labs",30,"Pain & fever","10 tablets"),
("Calpol 500","Paracetamol 500 mg","Haleon",22,"Pain & fever","10 tablets"),
("Crocin Advance","Paracetamol","Haleon",25,"Pain & fever","15 tablets"),
("Combiflam","Ibuprofen + Paracetamol","Sanofi",40,"Pain relief","10 tablets"),
("Brufen 400","Ibuprofen 400 mg","Abbott",38,"Pain relief","10 tablets"),
("Zerodol-P","Aceclofenac + Paracetamol","Ipca Laboratories",65,"Pain relief","10 tablets"),
("Volini Gel","Topical pain relief gel","Sun Pharma",115,"External use","30 g"),
("Moov Cream","Topical pain relief cream","Reckitt",110,"External use","50 g"),
("Allegra 120","Fexofenadine 120 mg","Sanofi",150,"Allergy care","10 tablets"),
("Cetcip 10","Cetirizine 10 mg","Cipla",28,"Allergy care","10 tablets"),
("Okacet","Cetirizine 10 mg","Cipla",25,"Allergy care","10 tablets"),
("Montair-LC","Montelukast + Levocetirizine","Cipla",105,"Allergy care","10 tablets"),
("Cofsils","Throat lozenges","Cipla",35,"Throat care","Pack"),
("Strepsils","Throat lozenges","Reckitt",45,"Throat care","Pack"),
("Digene","Antacid tablets","Abbott",35,"Digestive care","15 tablets"),
("Gelusil MPS","Antacid / antiflatulent","Pfizer",42,"Digestive care","10 tablets"),
("ENO","Antacid powder","Haleon",10,"Digestive care","Single sachet"),
("Pantocid 40","Pantoprazole 40 mg","Sun Pharma",105,"Digestive care","10 tablets"),
("Pan-D","Pantoprazole + Domperidone","Alkem",115,"Digestive care","10 capsules"),
("Econorm","Probiotic","Dr. Reddy's",95,"Digestive care","10 capsules"),
("Electral","ORS powder","FDC",22,"Hydration","1 sachet"),
("ORSL","Oral rehydration drink","Dabur",35,"Hydration","200 ml"),
("Zincovit","Multivitamin / multimineral","Apex Laboratories",105,"Vitamins","15 tablets"),
("Limcee 500","Vitamin C 500 mg","Abbott",30,"Vitamins","15 tablets"),
("Celin 500","Vitamin C 500 mg","Koye Pharmaceuticals",28,"Vitamins","10 tablets"),
("Supradyn","Multivitamin","Bayer",55,"Vitamins","15 tablets"),
("Shelcal 500","Calcium + Vitamin D3","Torrent Pharma",135,"Vitamins","15 tablets"),
("Calcimax Forte","Calcium supplement","Meyer Organics",145,"Vitamins","30 tablets"),
("Neurobion Forte","Vitamin B complex","P&G Health",42,"Vitamins","30 tablets"),
("Becosules","Vitamin B complex","Pfizer",45,"Vitamins","20 capsules"),
("Revital H","Multivitamin supplement","Sun Pharma",120,"Vitamins","10 capsules"),
("ORS-L","ORS sachet","Sample generic listing",20,"Hydration","1 sachet"),
("Betadine Ointment","Povidone-iodine topical","Win-Medicare",95,"First aid","20 g"),
("Savlon Antiseptic","Antiseptic liquid","ITC",95,"First aid","100 ml"),
("Dettol Antiseptic","Antiseptic liquid","Reckitt",85,"First aid","100 ml"),
("Band-Aid","Adhesive bandages","Johnson & Johnson",45,"First aid","Pack"),
("Hansaplast","Adhesive bandages","Beiersdorf",40,"First aid","Pack"),
("Cotton Roll","Medical cotton","Romsons",35,"First aid","25 g"),
("Crepe Bandage","Elastic support bandage","Vissco",95,"First aid","1 roll"),
("Digital Thermometer","Digital thermometer","Dr. Morepen",150,"Devices","1 unit"),
("BP Monitor","Digital blood pressure monitor","Omron",1650,"Devices","1 unit"),
("Glucometer Strips","Blood glucose test strips","Accu-Chek",650,"Devices","Pack"),
("Pregnancy Test Kit","Home pregnancy test","Prega News / Mankind",55,"Test kits","1 kit"),
("N95 Mask","Protective face mask","Venus",25,"Protection","1 mask"),
("Hand Sanitizer","Alcohol-based sanitizer","Lifebuoy / Unilever",55,"Protection","100 ml"),
("Vicks VapoRub","Topical vapour rub","P&G",55,"Cold care","25 ml"),
("Nasivion Adult","Nasal decongestant","Procter & Gamble",85,"Cold care","10 ml"),
("Otrivin Adult","Nasal spray","Haleon",95,"Cold care","10 ml"),
("Vicks Inhaler","Nasal inhaler","P&G",65,"Cold care","1 unit"),
("Benadryl Cough Syrup","Cough syrup","Johnson & Johnson",115,"Cough care","100 ml"),
("Ascoril LS","Cough syrup","Glenmark",125,"Cough care","100 ml"),
("Alex Syrup","Cough syrup","Glenmark",110,"Cough care","100 ml"),
("Honitus","Herbal cough syrup","Dabur",105,"Cough care","100 ml"),
("Lacto Calamine","Skin lotion","Piramal",125,"Skin care","120 ml"),
("Boroline","Antiseptic cream","G.D. Pharmaceuticals",45,"Skin care","20 g"),
("Himalaya Antiseptic Cream","Skin cream","Himalaya Wellness",70,"Skin care","20 g"),
("Clotrimazole Cream","Topical antifungal","Sample generic listing",35,"Skin care","15 g"),
("ORS + Thermometer Combo","Hydration and monitoring bundle","MediBill sample bundle",160,"Bundles","Combo"),
("First Aid Starter Pack","Bandage + antiseptic + cotton","MediBill sample bundle",155,"Bundles","Combo"),
("Vitamin C + Zinc Combo","Vitamin supplement bundle","MediBill sample bundle",125,"Bundles","Combo"),
]
PRODUCTS = {r[0]: {"generic":r[1],"company":r[2],"price":float(r[3]),"category":r[4],"pack":r[5]} for r in ROWS}
BUNDLES = {
    "First Aid Starter Pack":{"items":{"Band-Aid":1,"Betadine Ointment":1,"Cotton Roll":1},"discount":.05},
    "Hydration & Monitoring":{"items":{"Electral":2,"Digital Thermometer":1},"discount":.05},
    "Everyday Vitamins":{"items":{"Limcee 500":1,"Neurobion Forte":1},"discount":.05},
}
PROVIDERS = {"MediBill sample":1.00,"Tata 1mg estimate":1.04,"PharmEasy estimate":.98,"Apollo 24|7 estimate":1.02}
DELIVERY = {"Standard delivery (2–4 hours)":25.0,"Express delivery (within 90 minutes)":60.0,"Scheduled delivery":20.0,"Store pickup":0.0}

def money(value):
    return f"₹{value:,.2f}"

def calculate_bill(cart, rate, delivery_fee, membership):
    subtotal = sum(PRODUCTS[name]["price"] * qty for name, qty in cart.items())
    discount = subtotal * rate
    member_discount = min(10.0, subtotal - discount) if membership else 0.0
    return {"subtotal":subtotal,"discount":discount,"membership":member_discount,
            "delivery":delivery_fee,"total":max(0.0,subtotal-discount-member_discount+delivery_fee)}

def maps_url(location):
    query = f"pharmacies near {location}" if location.strip() else "pharmacies near me"
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(query)

def add_bundle(items):
    for name, qty in items.items():
        key = "qty_" + name
        st.session_state[key] = min(100, int(st.session_state.get(key,0)) + qty)

def paper_receipt(cart, bill, discount_name, delivery_name, customer, payment):
    bill_no = datetime.now().strftime("MB%y%m%d%H%M%S")
    rows = ""
    for i, (name, qty) in enumerate(cart.items(), 1):
        p = PRODUCTS[name]
        rows += f"<tr><td>{i}</td><td>{escape(name)}<br><small>{escape(p['generic'])}</small></td><td>{qty}</td><td>{p['price']:.2f}</td><td>{p['price']*qty:.2f}</td></tr>"
    if not rows:
        rows = "<tr><td colspan='5' style='text-align:center;padding:14px'>No items added</td></tr>"
    return f"""
    <div class="paper">
    <div class="rtitle">MEDIBILL PHARMACY</div><div class="rcenter">SAMPLE CASH MEMO / BILL</div>
    <div class="rcenter">Educational demonstration only</div><div class="rline"></div>
    <div>Bill No: {bill_no}</div><div>Date: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}</div>
    <div>Customer: {escape(customer or "Walk-in customer")}</div><div>Payment: {escape(payment)}</div>
    <div class="rline"></div>
    <table class="rtable"><thead><tr><th>#</th><th>Item description</th><th>Qty</th><th>Rate</th><th>Amt</th></tr></thead><tbody>{rows}</tbody></table>
    <div class="rline"></div>
    <div style="display:flex;justify-content:space-between"><span>Subtotal</span><span>{bill['subtotal']:.2f}</span></div>
    <div style="display:flex;justify-content:space-between"><span>Discount ({escape(discount_name)})</span><span>-{bill['discount']:.2f}</span></div>
    <div style="display:flex;justify-content:space-between"><span>Membership benefit</span><span>-{bill['membership']:.2f}</span></div>
    <div style="display:flex;justify-content:space-between"><span>Delivery ({escape(delivery_name)})</span><span>{bill['delivery']:.2f}</span></div>
    <div class="rline"></div><div class="rtotal"><span>TOTAL DUE</span><span>₹{bill['total']:.2f}</span></div>
    <div class="rline"></div><small>Sample data only. Verify product details and prices with a licensed pharmacy.</small>
    <div class="rcenter" style="margin-top:10px">Thank you. Please keep this receipt.</div>
    <div style="margin-top:14px">Signature: ________________________</div></div>
    """

for name in PRODUCTS:
    if "qty_"+name not in st.session_state:
        st.session_state["qty_"+name] = 0

with st.sidebar:
    st.markdown("## Order settings")
    customer = st.text_input("Customer name", placeholder="Walk-in customer")
    discount_name = st.selectbox("Discount",["No discount","5% off","10% off"])
    rate = {"No discount":0.0,"5% off":.05,"10% off":.10}[discount_name]
    membership = st.checkbox("Membership benefit (₹10 off)")
    delivery_name = st.selectbox("Delivery method",list(DELIVERY.keys()))
    delivery_fee = DELIVERY[delivery_name]
    payment = st.selectbox("Payment method",["Cash","UPI","Card","Pay on delivery"])
    area = st.text_input("Area or PIN code",placeholder="Enter location")
    st.link_button("Find nearby pharmacies",maps_url(area),use_container_width=True)
    st.caption("Opens Google Maps. This app does not access GPS or verify live stock.")

shop_tab, receipt_tab, bundles_tab, compare_tab, nearby_tab = st.tabs(
    ["Shop products","Paper receipt","Bundles","Price comparison","Nearby pharmacies"])

with shop_tab:
    st.subheader("Product catalogue")
    st.caption(f"{len(PRODUCTS)} sample listings from multiple brands and companies. Prices and pack details are illustrative.")
    search = st.text_input("Search brand, generic, company, or category",placeholder="e.g. Dolo, Cipla, vitamins")
    categories = ["All categories"] + sorted({p["category"] for p in PRODUCTS.values()})
    category = st.selectbox("Category",categories)
    matches = [(n,p) for n,p in PRODUCTS.items()
               if search.lower() in f"{n} {p['generic']} {p['company']} {p['category']}".lower()
               and (category=="All categories" or p["category"]==category)]
    product_col, bill_col = st.columns([1.55,1],gap="large")
    with product_col:
        if not matches:
            st.info("No matching products. Try a different search.")
        for name,p in matches:
            with st.container(border=True):
                a,b,c = st.columns([2.5,1,1])
                with a:
                    st.markdown(f"**{name}**")
                    st.caption(f"{p['generic']} · {p['pack']}")
                    st.caption(f"{p['company']} | {p['category']}")
                with b:
                    st.markdown(f"**{money(p['price'])}**")
                    st.caption("Sample price")
                with c:
                    st.number_input("Qty",min_value=0,max_value=100,step=1,key="qty_"+name)
    with bill_col:
        cart = {n:int(st.session_state["qty_"+n]) for n in PRODUCTS if int(st.session_state["qty_"+n])>0}
        bill = calculate_bill(cart,rate,delivery_fee,membership)
        st.markdown("### Current bill")
        if cart:
            st.dataframe(pd.DataFrame([{"Product":n,"Qty":q,"Amount":money(PRODUCTS[n]["price"]*q)} for n,q in cart.items()]),
                         hide_index=True,use_container_width=True,height=300)
        else:
            st.info("Add products to start the bill.")
        st.metric("Subtotal",money(bill["subtotal"]))
        st.write(f"Discount: **−{money(bill['discount'])}**")
        st.write(f"Membership: **−{money(bill['membership'])}**")
        st.write(f"Delivery: **{money(bill['delivery'])}**")
        st.markdown(f"## Total: {money(bill['total'])}")
        if st.button("Clear cart",use_container_width=True):
            for n in PRODUCTS: st.session_state["qty_"+n]=0
            st.rerun()

with receipt_tab:
    st.subheader("Classic paper-style receipt")
    cart = {n:int(st.session_state["qty_"+n]) for n in PRODUCTS if int(st.session_state["qty_"+n])>0}
    bill = calculate_bill(cart,rate,delivery_fee,membership)
    st.markdown(paper_receipt(cart,bill,discount_name,delivery_name,customer,payment),unsafe_allow_html=True)
    st.caption("This is a sample cash memo design, not a legally compliant tax invoice. No GST or pharmacy licence details are fabricated.")
    rows = [{"Brand":n,"Generic":PRODUCTS[n]["generic"],"Company":PRODUCTS[n]["company"],"Pack":PRODUCTS[n]["pack"],
             "Quantity":q,"Unit Price":PRODUCTS[n]["price"],"Line Total":PRODUCTS[n]["price"]*q} for n,q in cart.items()]
    rows += [{"Brand":"Subtotal","Line Total":bill["subtotal"]},{"Brand":"Discount","Line Total":-bill["discount"]},
             {"Brand":"Membership benefit","Line Total":-bill["membership"]},{"Brand":"Delivery","Line Total":bill["delivery"]},
             {"Brand":"TOTAL","Line Total":bill["total"]}]
    st.download_button("Download receipt as CSV",pd.DataFrame(rows).to_csv(index=False).encode("utf-8"),
                       file_name="medibill_receipt.csv",mime="text/csv",use_container_width=True)

with bundles_tab:
    st.subheader("Frequently bought together: demo bundles")
    st.caption("Manually configured examples, not real customer purchase-history recommendations or medical advice.")
    cols = st.columns(3)
    for i,(bundle,details) in enumerate(BUNDLES.items()):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"### {bundle}")
                subtotal = sum(PRODUCTS[n]["price"]*q for n,q in details["items"].items())
                st.markdown(f"**{money(subtotal*(1-details['discount']))}**")
                st.caption("Includes 5% illustrative bundle discount.")
                for n,q in details["items"].items(): st.write(f"- {n} × {q}")
                if st.button("Add bundle",key="bundle_"+bundle,use_container_width=True):
                    add_bundle(details["items"])
                    st.success("Added. Review in Shop products or Paper receipt.")

with compare_tab:
    st.subheader("Sample basket price comparison")
    st.warning("Provider prices are simulated estimates, not live or verified quotes.")
    selected = st.multiselect("Select products",list(PRODUCTS),default=["Dolo 650","Electral","Band-Aid"])
    if selected:
        rows=[]
        for name in selected:
            p=PRODUCTS[name]; base=p["price"]
            row={"Product":name,"Company":p["company"]}
            for provider,multiplier in PROVIDERS.items(): row[provider]=round(base*multiplier,2)
            row["Lowest sample price"]=min(round(base*m,2) for m in PROVIDERS.values())
            rows.append(row)
        df=pd.DataFrame(rows)
        numeric=[c for c in df.columns if c not in ["Product","Company"]]
        st.dataframe(df.style.format({c:"₹{:.2f}" for c in numeric}),hide_index=True,use_container_width=True)
        totals={provider:sum(PRODUCTS[n]["price"]*mult for n in selected) for provider,mult in PROVIDERS.items()}
        cols=st.columns(len(totals))
        for i,(provider,total) in enumerate(totals.items()):
            with cols[i]: st.metric(provider,money(total))
        cheapest=min(totals,key=totals.get)
        st.success(f"Lowest illustrative basket: {cheapest}, {money(totals[cheapest])}. This is not a real provider quote.")
    st.markdown("Provider websites: [Tata 1mg](https://www.1mg.com/) · [PharmEasy](https://pharmeasy.in/) · [Apollo 24|7](https://www.apollo247.com/)")
    st.caption("Verify exact brand, strength, pack size, stock, discount, delivery fee, and date for a fair comparison.")

with nearby_tab:
    st.subheader("Nearby pharmacies")
    pharmacy_area=st.text_input("Area or PIN code",value=area,key="pharmacy_area")
    st.write("Search on Google Maps. MediBill does not access GPS, show live stock, or verify opening hours.")
    st.link_button("Search pharmacies on Google Maps",maps_url(pharmacy_area),use_container_width=True)
    st.markdown("- [Tata 1mg](https://www.1mg.com/)")
    st.markdown("- [PharmEasy](https://pharmeasy.in/)")
    st.markdown("- [Apollo 24|7](https://www.apollo247.com/)")

st.markdown("---")
st.caption("MediBill is an academic prototype. Product names, company labels, pack details, prices, discounts, and delivery fees are illustrative and may be inaccurate. Verify with a licensed pharmacy. This app does not provide medical advice, prescriptions, GST calculation, or payment processing.")
