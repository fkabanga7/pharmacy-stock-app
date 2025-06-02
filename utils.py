import pandas as pd

def load_data():
    stock_path = "/Users/FabriceDiamant/Downloads/pharmacy_stock_app/data/pharmacy_stock.xlsx"
    log_path = "/Users/FabriceDiamant/Downloads/pharmacy_stock_app/data/stock_log.xlsx"

    try:
        stock_df = pd.read_excel(stock_path)
    except FileNotFoundError:
        stock_df = pd.DataFrame(columns=["Product ID", "Nom Produit", "Quantité", "Stock Value", "Reorder Level"])

    try:
        stock_log_df = pd.read_excel(log_path)
    except FileNotFoundError:
        stock_log_df = pd.DataFrame(columns=["Product ID", "Date", "Quantity", "Direction", "Notes"])

    return stock_df, stock_log_df


def update_stock(stock_df, stock_log_df, product_id, qty, date, direction, notes):
    try:
        product_id_int = int(product_id)
    except ValueError:
        return stock_df, stock_log_df, False

    product_idx = stock_df[stock_df['Product ID'] == product_id_int].index

    if product_idx.empty:
        # Product not found
        return stock_df, stock_log_df, False

    current_qty = stock_df.loc[product_idx, 'Quantité'].values[0]
    new_qty = current_qty + qty

    if new_qty < 0:
        # Prevent negative stock
        return stock_df, stock_log_df, False

    stock_df.loc[product_idx, 'Quantité'] = new_qty

    # Update log
    new_log = {
        "Product ID": product_id_int,
        "Date": date,
        "Quantity": qty,
        "Direction": direction,
        "Notes": notes
    }
    stock_log_df = pd.concat([stock_log_df, pd.DataFrame([new_log])], ignore_index=True)

    return stock_df, stock_log_df, True


def generate_dashboard(stock_df):
    total_products = len(stock_df)
    total_value = (stock_df['Quantité'] * stock_df['Stock Value']).sum() if not stock_df.empty else 0
    low_stock = len(stock_df[stock_df['Quantité'] < stock_df['Reorder Level']]) if not stock_df.empty else 0

    return {
        "total_products": total_products,
        "total_value": total_value,
        "low_stock": low_stock
    }
