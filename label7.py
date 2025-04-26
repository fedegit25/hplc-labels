import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
import barcode
from barcode.writer import ImageWriter
import io
import zipfile
import os

st.set_page_config(page_title="HPLC Sample Name Generator", layout="centered")

st.title("🔬 HPLC Sample Name Generator with Scannable Barcodes")

# --- Initialize session state ---
if "names" not in st.session_state:
    st.session_state.names = []
if "barcode_codes" not in st.session_state:
    st.session_state.barcode_codes = []
if "barcode_images" not in st.session_state:
    st.session_state.barcode_images = []
if "barcode_filenames" not in st.session_state:
    st.session_state.barcode_filenames = []

# --- Inputs ---
st.subheader("📋 Input Parameters")

today = datetime.today().strftime("%Y%m%d")
date = st.text_input("Date (YYYYMMDD)", value=today)
project = st.text_input("Project Name", value="ProjectX")
injection_start = st.number_input("Starting Injection Number", min_value=1, value=1)
num_samples = st.number_input("Number of Samples", min_value=1, value=10)
sample_base = st.text_input("Sample Base Name", value="SampleA")
mode = st.text_input("Mode", value="Positive")
volume = st.number_input("Sample Volume (µL)", min_value=1, value=10)

# --- Generate Names ---
if st.button("Generate Sample Names"):
    names = []
    barcode_codes = []
    barcode_images = []
    barcode_filenames = []

    for i in range(num_samples):
        barcode_code = str(uuid.uuid4().int)[:12]  # 12-digit unique code
        inj_num = f"{injection_start + i:02d}"
        sample_name = f"{sample_base}{i+1}"
        # --> include volume directly in the sample name
        full_name = f"{date}_{project}_{inj_num}_{sample_name}_{mode}_{volume}uL"

        names.append(full_name)
        barcode_codes.append(barcode_code)

        # Generate barcode image
        CODE128 = barcode.get_barcode_class('code128')
        my_code = CODE128(barcode_code, writer=ImageWriter())
        buffer = io.BytesIO()
        my_code.write(buffer)
        buffer.seek(0)

        barcode_images.append(buffer)
        barcode_filenames.append(f"{full_name}.png")

    # Save to session state
    st.session_state.names = names
    st.session_state.barcode_codes = barcode_codes
    st.session_state.barcode_images = barcode_images
    st.session_state.barcode_filenames = barcode_filenames

# --- If names exist, show them ---
if st.session_state.names:
    df_new = pd.DataFrame({
        "Sample Name": st.session_state.names,
        "Barcode Code": st.session_state.barcode_codes,
        "Barcode Image File": st.session_state.barcode_filenames
    })

    st.success("✅ Sample names and barcodes ready!")

    # Show barcode previews
    for idx, name in enumerate(st.session_state.names):
        st.write(f"**{name}**")
        st.image(st.session_state.barcode_images[idx], width=300)

    # --- Save to master database ---
    master_csv_path = "hplc_master_database.csv"

    if os.path.exists(master_csv_path):
        df_master = pd.read_csv(master_csv_path)
        df_master = pd.concat([df_master, df_new], ignore_index=True)
    else:
        df_master = df_new

    df_master.to_csv(master_csv_path, index=False)

    # --- Download current batch ---
    csv = df_new.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Current Batch (CSV)", 
        data=csv, 
        file_name="hplc_current_batch.csv", 
        mime="text/csv"
    )

    # --- Prepare ZIP file with barcode images ---
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for idx, buffer in enumerate(st.session_state.barcode_images):
            zip_file.writestr(st.session_state.barcode_filenames[idx], buffer.getvalue())
    zip_buffer.seek(0)

    st.download_button(
        "📦 Download All Barcodes as ZIP",
        data=zip_buffer,
        file_name="hplc_barcodes.zip",
        mime="application/zip"
    )
