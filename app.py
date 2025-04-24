import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="HPLC Sample Name Generator", layout="centered")

st.title("🔬 HPLC Sample Name Generator")

# --- Inputs ---
st.subheader("📋 Input Parameters")

today = datetime.today().strftime("%Y%m%d")
date = st.text_input("Date (YYYYMMDD)", value=today)
project = st.text_input("Project Name", value="ProjectX")
injection_start = st.number_input("Starting Injection Number", min_value=1, value=1)
num_samples = st.number_input("Number of Samples", min_value=1, value=10)
sample_base = st.text_input("Sample Base Name", value="SampleA")
mode = st.text_input("Mode", value="Positive")

# --- Generate Names ---
if st.button("Generate Sample Names"):
    names = []
    for i in range(num_samples):
        inj_num = f"{injection_start + i:02d}"
        sample_name = f"{sample_base}{i+1}"
        full_name = f"{date}_{project}_{inj_num}_{sample_name}_{mode}"
        names.append(full_name)

    df = pd.DataFrame(names, columns=["Sample Name"])
    
    st.success("✅ Sample names generated!")
    st.dataframe(df, use_container_width=True)
    
    # Download CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download as CSV", data=csv, file_name="hplc_sample_names.csv", mime="text/csv")
