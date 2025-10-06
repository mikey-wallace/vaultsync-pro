import streamlit as st
import pandas as pd

st.set_page_config(page_title="VaultSync Pro", layout="wide")
st.title("📊 VaultSync Pro — Week 6 Dashboard")

# Load data safely
try:
    df = pd.read_csv("data.csv")
except Exception:
    st.error("⚠️ Could not load data.csv. Please confirm the file exists and is properly formatted.")
    st.stop()

# Filter by Week 6
week6 = df[df["Tags"].str.contains("#Week6", na=False)]

# Group by Day
for day in week6["Date"].unique():
    st.subheader(f"📅 {day}")
    day_data = week6[week6["Date"] == day]

    income = day_data[day_data["Type"] == "Income"]["Amount"].sum()
    bills = day_data[day_data["Type"] == "Bill"]["Amount"].sum()
    buffer = income - bills

    st.markdown(f"**📥 Income:** ${income:,.2f}")
    st.markdown(f"**📤 Bills:** ${bills:,.2f}")
    st.markdown(f"**💰 Buffer:** ${buffer:,.2f}")

    with st.expander("🔍 View Entries"):
        display = day_data.copy()
        display["Amount"] = display["Amount"].apply(lambda x: f"${x:,.2f}")
        st.dataframe(display[["Vendor", "Amount", "Notes", "Tags"]])

# Divider
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

# Divider
st.markdown("---")
st.header("📤 Export Week 6 Digest")

if st.button("Generate Markdown Digest"):
    digest = week6.copy()
    digest["Amount"] = digest["Amount"].apply(lambda x: f"${x:,.2f}")
    md_lines = ["### VaultSync Pro — Week 6 Digest\n"]
    for day in digest["Date"].unique():
        md_lines.append(f"#### {day}")
        day_data = digest[digest["Date"] == day]
        for _, row in day_data.iterrows():
            md_lines.append(f"- **{row['Vendor']}**: {row['Amount']} — {row['Notes']} ({row['Tags']})")
        md_lines.append("")  # spacing
    st.code("\n".join(md_lines), language="markdown")

# Divider
st.markdown("---")
st.header("📝 Correct an Entry")

with st.form("correction_form"):
    index = st.number_input("Row index to correct (check entry viewer)", min_value=0, max_value=len(df)-1, step=1)
    field = st.selectbox("Field to correct", ["Date", "Vendor", "Amount", "Notes", "Tags", "Type"])
    new_value = st.text_input("New value")
    correct = st.form_submit_button("Apply Correction")

    if correct:
        df.at[index, field] = new_value if field != "Amount" else float(new_value)
        df.to_csv("data.csv", index=False)
        st.success(f"✅ Row {index} updated: {field} → {new_value}")

# Divider
st.markdown("---")
st.header("🔄 Start Week 7")

if st.button("Reset for Week 7"):
    df["Tags"] = df["Tags"].apply(lambda t: t.replace("#Week6", "#Week7") if "#Week6" in t else t)
    df.to_csv("data.csv", index=False)
    st.success("✅ Tags updated to #Week7. Dashboard will reflect new entries.")
