import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

st.set_page_config(page_title="Zomato Data Analysis", layout="wide")
st.title("🍽️ Zomato Restaurant Data Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload your Zomato CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    df = df.drop(['url','address','online_order','book_table','phone','rest_type',
                  'dish_liked','reviews_list','menu_item','listed_in(type)',
                  'listed_in(city)'], axis=1)

    df = df.rename(columns={'approx_cost(for two people)':'approx_cost'})
    df = df.fillna(0)

    df.approx_cost = df.approx_cost.replace('[,]', '', regex=True).astype('int64')
    df.rate = df.rate.replace('[/5]', '', regex=True)
    df.rate = df.rate.replace('NEW', 0)
    df.rate = df.rate.replace('-', 0).astype('float64')

    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    st.subheader("📍 Select Location")
    selected_location = st.selectbox("Choose:", sorted(df.location.unique()))
    lo = df[df.location == selected_location]

    st.write(f"### Restaurants in **{selected_location}**")
    st.dataframe(lo)

    grouped = lo.groupby('name')[['rate','approx_cost']].mean().nlargest(10,'rate').reset_index()

    st.subheader(f"⭐ Top 10 Restaurants in {selected_location}")
    st.dataframe(grouped)

    st.subheader("📊 Cost of Top Restaurants")
    plt.figure(figsize=(20, 8))
    sb.barplot(x=grouped.name, y=grouped.approx_cost, palette='summer')
    plt.xticks(rotation=90)
    st.pyplot(plt)

else:
    st.warning("⚠ Please upload your CSV file to continue.")

