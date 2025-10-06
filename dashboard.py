import streamlit as st
import pandas as pd
from modules.vaultsync import update_buffer
from modules.digest import generate_digest
from modules.log import log_transaction

FILEPATH = 'data.csv'

st.set_page_config(page_title="VaultSync Pro", layout="wide")
st.title("💼 VaultSync Pro Dashboard")

# Load data
try:
    df = pd.read_csv(FILEPATH)
except FileNotFoundError:
    st.warning("No data found. Add transactions below to begin.")
    df = pd.DataFrame(columns=[
        'Date', 'Type', 'Source/Vendor', 'Amount',
        'Status', 'Notes', 'Week', 'Buffer'
    ])

# Show buffer chart
if not df.empty:
    st.subheader("📊 Buffer Trend")
    st.line_chart(df['Buffer'])

# Show transaction table
st.subheader("📋 Transactions")
st.dataframe(df)

# Log new transaction
st.subheader("➕ Add Transaction")
col1, col2, col3 = st.columns(3)
with col1:
    tx_type = st.selectbox("Type", ["Income", "Bill"])
with col2:
    source = st.text_input("Source/Vendor")
with col3:
    amount = st.number_input("Amount", step=1.0)

status = st.selectbox("Status", ["Confirmed", "Pending"])
notes = st.text_input("Notes")

if st.button("Log Transaction"):
    entry = {
        'Type': tx_type,
        'Source/Vendor': source,
        'Amount': amount,
        'Status': status,
        'Notes': notes
    }
    log_transaction(FILEPATH, entry)
    st.success(f"{tx_type} logged for {source} — ${amount}")

# Update buffer
if st.button("🔄 Update Buffer"):
    final_buffer = update_buffer(FILEPATH)
    st.info(f"Buffer updated. Final total: ${final_buffer}")

# Generate digest
if st.button("🧾 Generate Digest"):
    digest = generate_digest(FILEPATH)
    st.text_area("Markdown Digest", digest, height=300)
