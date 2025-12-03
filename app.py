import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

# Streamlit page setup
st.set_page_config(page_title="Zomato Data Analysis", layout="wide")

st.title("🍽️ Zomato Restaurant Data Analysis")

# Load dataset
df = pd.read_csv('./Datasets/Zomato_Live.csv')

# Cleaning
df = df.drop(['url','address','online_order','book_table','phone','rest_type',
              'dish_liked','reviews_list','menu_item','listed_in(type)',
              'listed_in(city)'], axis=1)

df = df.rename(columns={'approx_cost(for two people)':'approx_cost'})
df = df.fillna(0)

df.approx_cost = df.approx_cost.replace('[,]', '', regex=True).astype('int64')
df.rate = df.rate.replace('[/5]', '', regex=True)
df.rate = df.rate.replace('NEW', 0)
df.rate = df.rate.replace('-', 0).astype('float64')

# Show dataset
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

# Location selection
st.subheader("📍 Select a Location")
selected_location = st.selectbox("Choose Location:", sorted(df.location.unique()))

# Filter by location
lo = df[df.location == selected_location]

st.write(f"### Restaurants in **{selected_location}**")
st.dataframe(lo)

# Grouped Results
grouped = lo.groupby('name')[['rate', 'approx_cost']].mean().nlargest(10, 'rate').reset_index()

st.subheader(f"⭐ Top 10 Restaurants in {selected_location} (Based on Rating)")
st.dataframe(grouped)

# Bar Plot
st.subheader("📊 Approx Cost of Top 10 Rated Restaurants")

plt.figure(figsize=(20, 8))
sb.barplot(x=grouped.name, y=grouped.approx_cost, palette='summer')
plt.xticks(rotation=90)
plt.xlabel("Restaurant Name")
plt.ylabel("Approx Cost")
plt.title(f"Top Restaurants by Cost in {selected_location}")

st.pyplot(plt)

