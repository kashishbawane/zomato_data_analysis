import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

st.set_page_config(page_title="Zomato Location Analysis", layout="wide")

st.title("🍽️ Zomato Location-wise Restaurant Analysis")

# Load dataset
df = pd.read_csv('./Datasets/Zomato_Live.csv')

# Show available locations
st.subheader("📍 Available Locations")
st.write(df.location.unique())

# Select location
location = st.selectbox("Select Location:", sorted(df.location.unique()))

# Filter data
lo = df[df.location == location]

# Grouping
gr = (
    lo.groupby('name')[['rate', 'approx_cost']]
    .mean()
    .nlargest(10, 'rate')
    .reset_index()
)

st.subheader(f"Top 10 Restaurants in {location} by Rating")
st.dataframe(gr)

# Plot Bar Chart
st.subheader("📊 Approx. Cost of Top 10 Restaurants")

plt.figure(figsize=(20, 8))
sb.barplot(x=gr.name, y=gr.approx_cost, palette='summer')
plt.xticks(rotation=90)

st.pyplot(plt)
