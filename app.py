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
                        image_file = (
                            PRODUCT_IMAGES.get(name)
                            or CATEGORY_IMAGES.get(item["category"])
                            or "medicine_blister_packs.png"
                        )
                        image_path = asset_path(image_file)

                        if image_path:
                            st.image(image_path, use_container_width=True)
                        else:
                            st.markdown(
                                "<div style='height:120px;display:flex;align-items:center;"
                                "justify-content:center;background:#EEF2F6;border-radius:10px;"
                                "color:#64748B;font-size:14px;'>Product image unavailable</div>",
                                unsafe_allow_html=True,
                            )
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
        st.button("Clear cart", use_container_width=True, on_click=clear_cart)

with bundles_tab:
    st.subheader("Convenience bundles")
    st.write("Example groupings only. They are not medical recommendations or derived from real purchase history.")
    cols = st.columns(2)
    for i,(bundle_name,items) in enumerate(BUNDLES.items()):
        with cols[i%2]:
            with st.container(border=True):
                bundle_image = {
                    "First-Aid Basics": "first_aid_bandage.png",
                    "Hydration Supplies": "ors_packet.png",
                    "Home Monitoring": "digital_thermometer.png",
                    "Everyday Personal Care": "petroleum_jelly.png",
                }.get(bundle_name)
                bundle_image_path = asset_path(bundle_image) if bundle_image else None
                if bundle_image_path:
                    st.image(bundle_image_path, use_container_width=True)
                st.markdown(f"#### {bundle_name}")
                total = sum(PRODUCTS[n]["price"]*q for n,q in items.items())
                st.markdown(f"**Sample bundle total: {money(total*0.95)}**")
                st.caption("Includes an illustrative 5% bundle discount.")
                for name,qty in items.items():
                    st.write(f"- {name} × {qty}")
                st.button(
                    "Add bundle to cart",
                    key="bundle_" + bundle_name,
                    use_container_width=True,
                    on_click=add_bundle,
                    args=(items,),
                )
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
