import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

st.set_page_config(page_title="Zomato Data Analysis", layout="wide")
st.title("🍽️ Zomato Location-wise Restaurant Analysis")

# Upload CSV
uploaded_file = st.file_uploader("📤 Upload Zomato CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📍 Available Locations")
    st.write(df.location.unique())

    location = st.selectbox("Select Location:", sorted(df.location.unique()))
    lo = df[df.location == location]

    gr = (
        lo.groupby('name')[['rate', 'approx_cost']]
        .mean()
        .nlargest(10, 'rate')
        .reset_index()
    )

    st.subheader(f"Top 10 Restaurants in {location} by Rating")
    st.dataframe(gr)

    st.subheader("📊 Approx. Cost of Top 10 Restaurants")

    plt.figure(figsize=(20, 8))
    sb.barplot(x=gr.name, y=gr.approx_cost, palette='summer')
    plt.xticks(rotation=90)
    st.pyplot(plt)
else:
    st.warning("⚠ Please upload your CSV file to continue.")
