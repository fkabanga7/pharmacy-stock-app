# generate_sample_data.py
import pandas as pd
import os

data = {
    "Product ID": ["001", "002", "003"],
    "Nom Produit": ["Paracetamol 500mg", "Amoxicillin 250mg", "Ibuprofen 200mg"],
    "Quantité": [100, 80, 60],
    "Prix/Unit": [1.5, 2.0, 1.2],
    "Reorder Level": [20, 30, 15]
}

df = pd.DataFrame(data)

os.makedirs("data", exist_ok=True)
df.to_excel("/Users/FabriceDiamant/Downloads/pharmacy_stock_app/data/pharmacy_stock.xlsx", index=False)
print("Sample pharmacy_stock.xlsx created.")
