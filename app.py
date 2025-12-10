import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
import plotly.express as px

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="Zomato Animated Dashboard",
                   layout="wide",
                   page_icon="🍽️")

# ------------------- CUSTOM CSS -------------------
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
st.markdown("<h1 class='big-title'>🍽️ Zomato AI & Animated Analytics Dashboard</h1>", unsafe_allow_html=True)

# ------------------- FILE UPLOADER -------------------
uploaded_file = st.file_uploader("📤 Upload Zomato CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ---------- SIDEBAR FILTERS ----------
    st.sidebar.header("🔍 Filters Panel")

    min_rating, max_rating = st.sidebar.slider(
        "Filter by Rating",
        0.0, 5.0, (0.0, 5.0)
    )

    min_cost, max_cost = st.sidebar.slider(
        "Filter by Approx Cost",
        int(df.approx_cost.min()), int(df.approx_cost.max()),
        (int(df.approx_cost.min()), int(df.approx_cost.max()))
    )

    location = st.sidebar.selectbox("Select Location", sorted(df.location.unique()))
    search = st.sidebar.text_input("Search Restaurant Name")

    # ---------- APPLY FILTERS ----------
    lo = df[
        (df.location == location) &
        (df.rate.between(min_rating, max_rating)) &
        (df.approx_cost.between(min_cost, max_cost))
    ]

    if search:
        lo = lo[lo.name.str.contains(search, case=False)]

    # ---------- Metrics ----------
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("<div class='card'><h3>📍 Location</h3>", unsafe_allow_html=True)
        st.markdown(f"<h2>{location}</h2></div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='card'><h3>🏪 Restaurants Found</h3>", unsafe_allow_html=True)
        st.markdown(f"<h2>{len(lo)}</h2></div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='card'><h3>⭐ Best Rating</h3>", unsafe_allow_html=True)
        st.markdown(f"<h2>{round(lo.rate.max(),2)}</h2></div>", unsafe_allow_html=True)

    # AI Suggestion
    st.subheader("🤖 AI Recommendation")
    if len(lo) > 0:
        best = lo.sort_values("rate", ascending=False).iloc[0]
        st.success(f"💡 Best restaurant in **{location}** is **{best['name']}** "
                   f"with ⭐ **{best['rate']}**, Cost: ₹{best['approx_cost']}")
    else:
        st.warning("No restaurants found. Try different filters!")

    # ---------- Top 10 Restaurants ----------
    gr = lo.groupby('name')[['rate', 'approx_cost']].mean().nlargest(10, 'rate').reset_index()
    st.subheader(f"🏆 Top 10 Restaurants in {location}")
    st.dataframe(gr, use_container_width=True)

    # --------------------------------------------------
    # 🔥🔥🔥 ANIMATED CHART 1 — COST BAR CHART (Plotly) 🔥🔥🔥
    # --------------------------------------------------
    st.subheader("📊 Animated — Top Restaurants Approx Cost")

    fig_animated_cost = px.bar(
        gr,
        x="name",
        y="approx_cost",
        color="approx_cost",
        animation_frame="rate",
        title="Animated Cost Chart (based on Rating)",
        labels={"name": "Restaurant Name", "approx_cost": "Approx Cost"},
    )
    fig_animated_cost.update_layout(width=1000, height=500)
    st.plotly_chart(fig_animated_cost)

    # --------------------------------------------------
    # 🔥🔥🔥 ANIMATED CHART 2 — COST vs RATING (Bubble) 🔥🔥🔥
    # --------------------------------------------------
    st.subheader("🟢 Animated Bubble Chart — Cost vs Rating")

    fig_bubble = px.scatter(
        lo,
        x="approx_cost",
        y="rate",
        size="approx_cost",
        color="rate",
        hover_name="name",
        animation_frame="rate",
        title="Cost vs Rating (Animated)",
    )
    fig_bubble.update_layout(width=1000, height=500)
    st.plotly_chart(fig_bubble)

    # --------------------------------------------------
    # 🔥🔥🔥 HEATMAP (Static) 🔥🔥🔥
    # --------------------------------------------------
    st.subheader("🔥 Correlation Heatmap")

    fig4 = plt.figure(figsize=(6, 4))
    sb.heatmap(lo[['approx_cost', 'rate']].corr(), annot=True, cmap="magma")
    st.pyplot(fig4)

    # --------------------------------------------------
    # 🗺️ MAP VISUALIZATION
    # --------------------------------------------------
    st.subheader("🗺️ Restaurants Map")

    if "lat" in df.columns and "long" in df.columns:
        st.map(lo[['lat', 'long']])
    else:
        st.info("Map not available — lat/long missing in dataset.")

else:
    st.info("👆 Upload a Zomato CSV file to start the dashboard.")
