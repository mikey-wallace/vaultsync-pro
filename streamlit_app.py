import streamlit as st
import pandas as pd

st.set_page_config(page_title="VaultSync Pro", layout="wide")
st.title("📊 VaultSync Pro — Week 6 Dashboard")

# Load data
df = pd.read_csv("data.csv")

# Filter by Week 6
week6 = df[df["Tags"].str.contains("#Week6", na=False)]

# Group by Day
for day in week6["Date"].unique():
    st.subheader(f"📅 {day}")
    day_data = week6[week6["Date"] == day]

    income = day_data[day_data["Type"] == "Income"]["Amount"].sum()
    bills = day_data[day_data["Type"] == "Bill"]["Amount"].sum()
    buffer = income - bills

    st.markdown(f"**📥 Income:** ${income:.2f}")
    st.markdown(f"**📤 Bills:** ${bills:.2f}")
    st.markdown(f"**💰 Buffer:** ${buffer:.2f}")

    with st.expander("🔍 View Entries"):
        st.dataframe(day_data[["Vendor", "Amount", "Notes", "Tags"]])

# Add new entry
st.markdown("---")
st.header("➕ Add New Entry")

with st.form("new_entry"):
    date = st.text_input("Date (e.g. Tuesday, 7 October 2025)")
    vendor = st.text_input("Vendor")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    notes = st.text_input("Notes")
    tags = st.text_input("Tags (e.g. #Week6 #Confirmed)")
    entry_type = st.selectbox("Type", ["Income", "Bill"])
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        new_row = pd.DataFrame([{
            "Date": date,
            "Vendor": vendor,
            "Amount": amount,
            "Notes": notes,
            "Tags": tags,
            "Type": entry_type
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv("data.csv", index=False)
        st.success("✅ Entry added successfully. Refresh to see update.")
