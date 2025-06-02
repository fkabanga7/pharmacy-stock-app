# app.py
import streamlit as st
import pandas as pd
from utils import load_data, update_stock, generate_dashboard

# Load data
stock_df, stock_log_df = load_data()

st.set_page_config(page_title="Pharmacy Inventory", layout="wide")
st.title("💊 Pharmacy Stock Control App")

# Tabs
menu = st.sidebar.radio("Navigation", ["📦 Stock List", "➕ Stock In", "➖ Stock Out", "📊 Dashboard"])

if menu == "📦 Stock List":
    st.subheader("Product List")
    st.dataframe(stock_df)

elif menu == "➕ Stock In":
    st.subheader("Stock In")
    with st.form("stock_in_form"):
        product_id = st.selectbox("Select Product", stock_df['Product ID'])
        qty = st.number_input("Quantity In", min_value=1)
        date = st.date_input("Date")
        supplier = st.text_input("Supplier")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Submit")

    if submitted:
        stock_df, stock_log_df = update_stock(
            stock_df, stock_log_df, product_id, qty, date, "IN", notes
        )
        st.success("Stock updated successfully.")

elif menu == "➖ Stock Out":
    st.subheader("Stock Out")
    with st.form("stock_out_form"):
        product_id = st.selectbox("Select Product", stock_df['Product ID'])
        qty = st.number_input("Quantity Out", min_value=1)
        date = st.date_input("Date")
        purpose = st.text_input("Purpose")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Submit")

    if submitted:
        stock_df, stock_log_df = update_stock(
            stock_df, stock_log_df, product_id, -qty, date, "OUT", notes
        )
        st.success("Stock updated successfully.")

elif menu == "📊 Dashboard":
    st.subheader("Dashboard")
    metrics = generate_dashboard(stock_df)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Products", metrics['total_products'])
    col2.metric("Total Stock Value", f"${metrics['total_value']:,.2f}")
    col3.metric("Low Stock Items", metrics['low_stock'])

    st.dataframe(stock_df[stock_df['Quantité'] < stock_df['Reorder Level']])

# Optionally save updated data
stock_df.to_excel("data/pharmacy_stock.xlsx", index=False)
stock_log_df.to_excel("data/stock_log.xlsx", index=False)