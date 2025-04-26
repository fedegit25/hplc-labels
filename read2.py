import streamlit as st
import pandas as pd

# Load your CSV
df = pd.read_csv("hplc_master_database.csv")

# Make sure Barcode Code is treated as string
df["Barcode Code"] = df["Barcode Code"].astype(str)

st.title("🔎 HPLC Sample Lookup System")

barcode_input = st.text_input("📷 Scan or Type Barcode Code:")

if barcode_input:
    barcode_input = barcode_input.strip()  # Remove any extra spaces
    match = df[df["Barcode Code"] == barcode_input]

    if not match.empty:
        st.success("✅ Sample found!")
        st.dataframe(match)
    else:
        st.error("❌ No matching sample found. Try again.")
