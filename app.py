import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="Zomato Intelligent Dashboard",
                   layout="wide",
                   page_icon="🍽️")

# ------------------- CUSTOM UI CSS -------------------
st.markdown("""
<style>
.big-title {
    font-size: 50px;
    font-weight: bold;
    text-align: center;
    color: #ff4c4c;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #FFF7EB;
    text-align: center;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

# ------------------- TITLE -------------------
st.markdown("<h1 class='big-title'>🍽️ Zomato AI-Powered Analytics Dashboard</h1>", unsafe_allow_html=True)
st.write("Explore restaurants with **AI insights, advanced filters, beautiful charts & maps**")

# ------------------- FILE UPLOADER -------------------
uploaded_file = st.file_uploader("📤 Upload Zomato CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ------------- SIDEBAR FILTERS ----------------
    st.sidebar.header("🔍 Filters Panel")

    # Rating range filter
    min_rating, max_rating = st.sidebar.slider(
        "Filter by Rating (0 to 5)",
        0.0, 5.0, (0.0, 5.0)
    )

    # Cost filter
    min_cost, max_cost = st.sidebar.slider(
        "Filter by Approx Cost",
        int(df.approx_cost.min()), int(df.approx_cost.max()),
        (int(df.approx_cost.min()), int(df.approx_cost.max()))
    )

    # Location dropdown
    location = st.sidebar.selectbox("Select Location", sorted(df.location.unique()))

    # Restaurant search bar
    search = st.sidebar.text_input("Search Restaurant Name")

    # ---------------- FILTERING DATA -----------------
    lo = df[
        (df.location == location) &
        (df.rate.between(min_rating, max_rating)) &
        (df.approx_cost.between(min_cost, max_cost))
    ]

    if search:
        lo = lo[lo.name.str.contains(search, case=False)]

    # -------------------- METRICS --------------------
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("<div class='card'><h3>📍 Location</h3>", unsafe_allow_html=True)
        st.markdown(f"<h2>{location}</h2></div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='card'><h3>🏪 Restaurants Found</h3>", unsafe_allow_html=True)
        st.markdown(f"<h2>{len(lo)}</h2></div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='card'><h3>⭐ Highest Rating</h3>", unsafe_allow_html=True)
        st.markdown(f"<h2>{round(lo.rate.max(),2)}</h2></div>", unsafe_allow_html=True)

    # ------------------- AI RECOMMENDATION -------------------
    st.subheader("🤖 AI Recommendation")

    if len(lo) > 0:
        best = lo.sort_values("rate", ascending=False).iloc[0]
        st.success(f"💡 Best restaurant in **{location}** is **{best['name']}** "
                   f"with rating ⭐ **{best['rate']}** and cost **₹{best['approx_cost']}**")
    else:
        st.warning("No restaurants found for selected filters!")

    # ------------------- TOP 10 RESTAURANTS TABLE -------------------
    gr = lo.groupby('name')[['rate', 'approx_cost']].mean().nlargest(10, 'rate').reset_index()

    st.subheader(f"🏆 Top 10 Restaurants in {location}")
    st.dataframe(gr, use_container_width=True)

    # ------------------- CHART 1: COST BAR CHART -------------------
    st.subheader("📊 Top Restaurants - Approx Cost")

    fig = plt.figure(figsize=(16, 6))
    sb.barplot(x=gr.name, y=gr.approx_cost, palette="summer")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ------------------- CHART 2: RATING BAR CHART -------------------
    st.subheader("⭐ Top Restaurants - Ratings")

    fig2 = plt.figure(figsize=(16, 6))
    sb.barplot(x=gr.name, y=gr.rate, palette="coolwarm")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # ------------------- CHART 3: COST vs RATING SCATTER -------------------
    st.subheader("📌 Cost vs Rating (Trend Analysis)")

    fig3 = plt.figure(figsize=(10, 5))
    sb.scatterplot(data=lo, x="approx_cost", y="rate")
    plt.xlabel("Approx Cost")
    plt.ylabel("Rating")
    st.pyplot(fig3)

    # ------------------- CHART 4: HEATMAP -------------------
    st.subheader("🔥 Correlation Heatmap")

    fig4 = plt.figure(figsize=(6, 4))
    sb.heatmap(lo[['approx_cost', 'rate']].corr(), annot=True, cmap="magma")
    st.pyplot(fig4)

    # ------------------- MAP VISUALIZATION -------------------
    st.subheader("🗺️ Restaurants Map (If Latitude & Longitude available)")

    if "lat" in df.columns and "long" in df.columns:
        st.map(lo[['lat', 'long']])
    else:
        st.info("Map could not be displayed — No latitude/longitude columns found in your dataset.")

else:
    st.info("👆 Upload a Zomato CSV file to start the dashboard.")
