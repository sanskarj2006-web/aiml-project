import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Hospital Patient Waiting Time Analysis",
    page_icon="🏥",
    layout="wide"
)

# ---------------- TITLE ----------------
st.markdown(
    "<h1 style='text-align: center;'>🏥 Hospital Patient Waiting Time Analysis</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Statistical analysis of patient waiting times to evaluate hospital service efficiency</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

st.sidebar.markdown("**Required Column:** `Waiting_Time` (in minutes)")

# ---------------- MAIN LOGIC ----------------
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    st.dataframe(df.head(), use_container_width=True)

    if "Waiting_Time" in df.columns:
        # ---------------- STATISTICS ----------------
        mean_val = df["Waiting_Time"].mean()
        median_val = df["Waiting_Time"].median()
        std_val = df["Waiting_Time"].std()
        var_val = df["Waiting_Time"].var()

        st.subheader("📊 Statistical Summary")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Mean (min)", round(mean_val, 2))
        c2.metric("Median (min)", round(median_val, 2))
        c3.metric("Std Deviation", round(std_val, 2))
        c4.metric("Variance", round(var_val, 2))

        st.divider()

        # ---------------- LINE CHART ----------------
        st.subheader("📈 Waiting Time Trend")
        df["Index"] = range(len(df))
        fig_line = px.line(
            df,
            x="Index",
            y="Waiting_Time",
            title="Patient Waiting Time Trend",
            markers=True
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # ---------------- BOX PLOT ----------------
        st.subheader("📦 Waiting Time Distribution")
        fig_box = px.box(
            df,
            y="Waiting_Time",
            title="Box Plot of Waiting Times"
        )
        st.plotly_chart(fig_box, use_container_width=True)

        # ---------------- HISTOGRAM ----------------
        st.subheader("📊 Frequency Distribution")
        fig_hist = px.histogram(
            df,
            x="Waiting_Time",
            nbins=20,
            title="Histogram of Waiting Times"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

        # ---------------- INSIGHTS ----------------
        st.subheader("🧠 Insights")
        st.success(
            f"""
            • Average waiting time is **{round(mean_val,2)} minutes**  
            • High variance indicates **inconsistent service efficiency**  
            • Outliers in box plot suggest **peak-hour congestion**
            """
        )

    else:
        st.error("❌ CSV file must contain a column named `Waiting_Time`")

else:
    st.info("⬅️ Upload a CSV file from the sidebar to begin analysis.")
