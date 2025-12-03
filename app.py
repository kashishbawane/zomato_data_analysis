import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# -------------------- Page Setup --------------------
st.set_page_config(
    page_title="Zomato Data Explorer",
    layout="wide",
    page_icon="🍽️"
)

# Custom CSS for beauty
st.markdown("""
<style>
.big-title {
    font-size: 48px;
    font-weight: bold;
    text-align: center;
    color: #ff4c4c;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #FFF5EB;
    text-align: center;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# -------------------- Title --------------------
st.markdown("<h1 class='big-title'>🍽️ Zomato Data Interactive Dashboard</h1>", unsafe_allow_html=True)
st.write("### Explore restaurants by location, cost, and ratings — beautifully!")

# -------------------- Upload CSV --------------------
uploaded_file = st.file_uploader("📤 Upload Your Zomato CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # -------------------- Sidebar Filters --------------------
    st.sidebar.header("🔍 Filters")

    # Location filter
    location = st.sidebar.selectbox("Select Location:", sorted(df.location.unique()))

    # Filtered Data
    lo = df[df.location == location]

    # Group results
    gr = (
        lo.groupby('name')[['rate','approx_cost']]
        .mean()
        .nlargest(10, 'rate')
        .reset_index()
    )

    # -------------------- Metrics Cards --------------------
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("<div class='card'><h3>📍 Selected Location</h3>", unsafe_allow_html=True)
        st.markdown(f"<h2>{location}</h2></div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='card'><h3>⭐ Restaurants Count</h3>", unsafe_allow_html=True)
        st.markdown(f"<h2>{len(lo)}</h2></div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='card'><h3>🏆 Top Rating</h3>", unsafe_allow_html=True)
        st.markdown(f"<h2>{round(gr.rate.max(),2)}</h2></div>", unsafe_allow_html=True)

    # -------------------- Data Table --------------------
    st.subheader(f"🏅 Top 10 Restaurants in {location}")
    st.dataframe(gr, use_container_width=True)

    # -------------------- Bar Chart --------------------
    st.subheader("📊 Price Comparison of Top Restaurants")

    fig = plt.figure(figsize=(16, 7))
    sb.barplot(x=gr.name, y=gr.approx_cost, palette='viridis')
    plt.xticks(rotation=45, ha='right')
    plt.title(f"Approx Cost of Top Restaurants in {location}", fontsize=16)
    plt.xlabel("Restaurant Name")
    plt.ylabel("Approx Cost")

    st.pyplot(fig)

    # -------------------- Rating Chart --------------------
    st.subheader("⭐ Rating Comparison")

    fig2 = plt.figure(figsize=(16, 6))
    sb.barplot(x=gr.name, y=gr.rate, palette='coolwarm')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Rating")

    st.pyplot(fig2)

else:
    st.info("👆 Upload your Zomato CSV file to start exploring.")
