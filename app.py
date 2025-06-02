import streamlit as st
import pandas as pd
from utils import load_data, update_stock, generate_dashboard

# Initialize session state data
if "stock_df" not in st.session_state or "stock_log_df" not in st.session_state:
    stock_df, stock_log_df = load_data()
    st.session_state.stock_df = stock_df
    st.session_state.stock_log_df = stock_log_df

st.set_page_config(page_title="Pharmacy Inventory", layout="wide")
st.title("💊 Pharmacy Stock Control App")

stock_df = st.session_state.stock_df
stock_log_df = st.session_state.stock_log_df

# Create product display list for dropdowns
product_display_list = []
if not stock_df.empty and 'Product ID' in stock_df.columns and 'Nom Produit' in stock_df.columns:
    product_display_list = (stock_df['Product ID'].astype(str) + " - " + stock_df['Nom Produit']).tolist()

# Tabs
menu = st.sidebar.radio("Navigation", ["📦 Stock List", "➕ Add New Product", "➕ Stock In", "➖ Stock Out", "📊 Dashboard"])

if menu == "📦 Stock List":
    st.subheader("Product List")
    if stock_df.empty:
        st.warning("No products found. Please add stock.")
    else:
        st.dataframe(stock_df)

elif menu == "➕ Add New Product":
    st.subheader("Add New Product")
    with st.form("add_product_form"):
        product_id = st.text_input("Product ID")
        product_name = st.text_input("Nom Produit")
        quantity = st.number_input("Quantité initiale", min_value=0, value=0)
        stock_value = st.number_input("Stock Value (per unit)", min_value=0.0, format="%.2f", value=0.0)
        reorder_level = st.number_input("Reorder Level", min_value=0, value=0)
        submitted = st.form_submit_button("Add Product")

    if submitted:
        if product_id and product_name:
            try:
                product_id_int = int(product_id)
            except ValueError:
                st.error("Product ID must be an integer.")
            else:
                if product_id_int in stock_df['Product ID'].values:
                    st.error("Product ID already exists.")
                else:
                    new_product = {
                        "Product ID": product_id_int,
                        "Nom Produit": product_name,
                        "Quantité": quantity,
                        "Stock Value": stock_value,
                        "Reorder Level": reorder_level
                    }
                    st.session_state.stock_df = pd.concat([stock_df, pd.DataFrame([new_product])], ignore_index=True)
                    st.success(f"Product '{product_name}' added successfully.")
                    # Refresh display list
                    product_display_list.append(f"{product_id} - {product_name}")

elif menu == "➕ Stock In":
    st.subheader("Stock In")
    if stock_df.empty:
        st.warning("No products available. Please add stock via Add New Product tab.")
    else:
        with st.form("stock_in_form"):
            product_display = st.selectbox("Select Product", product_display_list)
            product_id = product_display.split(" - ")[0]
            qty = st.number_input("Quantity In", min_value=1, value=1)
            date = st.date_input("Date")
            supplier = st.text_input("Supplier")
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Submit")

        if submitted:
            updated_stock_df, updated_log_df, success = update_stock(
                st.session_state.stock_df, st.session_state.stock_log_df, product_id, qty, date, "IN", notes
            )
            if success:
                st.session_state.stock_df = updated_stock_df
                st.session_state.stock_log_df = updated_log_df
                st.success("Stock updated successfully.")
            else:
                st.error("Failed to update stock.")

elif menu == "➖ Stock Out":
    st.subheader("Stock Out")
    if stock_df.empty:
        st.warning("No products available. Please add stock via Add New Product tab.")
    else:
        with st.form("stock_out_form"):
            product_display = st.selectbox("Select Product", product_display_list)
            product_id = product_display.split(" - ")[0]
            qty = st.number_input("Quantity Out", min_value=1, value=1)
            date = st.date_input("Date")
            purpose = st.text_input("Purpose")
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Submit")

        if submitted:
            updated_stock_df, updated_log_df, success = update_stock(
                st.session_state.stock_df, st.session_state.stock_log_df, product_id, -qty, date, "OUT", notes
            )
            if success:
                st.session_state.stock_df = updated_stock_df
                st.session_state.stock_log_df = updated_log_df
                st.success("Stock updated successfully.")
            else:
                st.error("Insufficient stock. Cannot perform Stock Out.")

elif menu == "📊 Dashboard":
    st.subheader("Dashboard")
    if stock_df.empty:
        st.warning("No data available to generate dashboard.")
    else:
        metrics = generate_dashboard(stock_df)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Products", metrics['total_products'])
        col2.metric("Total Stock Value", f"${metrics['total_value']:,.2f}")
        col3.metric("Low Stock Items", metrics['low_stock'])

        st.dataframe(stock_df[stock_df['Quantité'] < stock_df['Reorder Level']])

# Save button to persist changes
if st.sidebar.button("Save Changes to Disk"):
    if not st.session_state.stock_df.empty:
        st.session_state.stock_df.to_excel("/Users/FabriceDiamant/Downloads/pharmacy_stock_app/data/pharmacy_stock.xlsx", index=False)
        st.session_state.stock_log_df.to_excel("/Users/FabriceDiamant/Downloads/pharmacy_stock_app/data/stock_log.xlsx", index=False)
        st.success("Data saved successfully!")
    else:
        st.warning("No data to save.")
