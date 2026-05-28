import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.markdown(
    """
    <style>

    .stApp {

        background-color: #F8FAFC;

        color: #111827;

        font-family: 'Segoe UI', sans-serif;
    }

    .block-container {

        padding-top: 3rem;

        padding-left: 6rem;

        padding-right: 6rem;
    }

    h1 {

        text-align: center;

    font-size: 56px !important;
}

.stFileUploader label {

    color: black !important;

    font-weight: 600;
}

.stFileUploader div {

    color: black !important;
    }

    h3 {

        text-align: center;

        color: #374151;

        font-size: 26px;

        font-weight: 600;
    }

    p {

        text-align: center;

        color: #6B7280;

        font-size: 16px;
    }

    section[data-testid="stSidebar"] {

        background-color: #FFFFFF;

        border-right: 1px solid #E5E7EB;

        min-width: 320px;

        max-width: 320px;
    }

    .stFileUploader {

    background-color: white !important;

    padding: 30px !important;

    border-radius: 20px !important;

    border: 1px solid #E5E7EB !important;
}

.stFileUploader label {

    color: black !important;

    font-size: 18px !important;

    font-weight: 700 !important;
}

.stFileUploader div {

    color: black !important;
}

.stFileUploader span {

    color: black !important;
}

.stFileUploader small {

    color: black !important;
}

    .stFileUploader {

        background-color: white;
 }

.stFileUploader span {

    color: black !important;

    font-weight: 600;
}

        border-radius: 24px;

        border: 1px solid #E5E7EB;

        box-shadow:
        0 8px 30px rgba(0,0,0,0.06);

        max-width: 700px;

        margin: auto;
    }

    div[data-testid="metric-container"] {

        background-color: white;

        border-radius: 24px;

        padding: 28px;

        border: 1px solid #E5E7EB;

        box-shadow:
        0 6px 24px rgba(0,0,0,0.05);
    }

    .stDataFrame {

        border-radius: 20px;

        overflow: hidden;

        border: 1px solid #E5E7EB;
    }

   .stFileUploader button {

    color: black !important;

    background-color: #2563EB !important;

    font-weight: 700 !important;
   }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("☁️ AI Dashboard")

st.sidebar.markdown("""
### Smart Forecasting

✔ Sales Analytics  
🤖 AI Predictions  
📂 CSV Upload  
📊 Business Insights  
""")

# =========================
# TITLE
# =========================

st.title("📈 Sales & Demand Forecasting Dashboard")

st.markdown("""
### 📊 Smart Business Forecasting Dashboard

Predict future sales trends using Artificial Intelligence & Machine Learning.
""")

# =========================
# FILE UPLOADER
# =========================

uploaded_file = st.file_uploader(
    "Upload Sales CSV File",
    type=["csv"]
)

# =========================
# MAIN APP
# =========================

if uploaded_file is not None:

    try:

        # Read CSV
        df = pd.read_csv(
            uploaded_file,
            encoding='latin1'
        )

        st.success("✅ Dataset Uploaded Successfully!")

        # =========================
        # BENTO GRID METRICS
        # =========================

        top_left, top_right = st.columns([2,1])

        with top_left:

            st.subheader("📦 Total Sales")

            st.metric(
                "",
                f"${df['Sales'].sum():,.0f}"
            )

        with top_right:

            st.subheader("🧾 Orders")

            st.metric(
                "",
                len(df)
            )

        bottom_left, bottom_right = st.columns([1,2])

        with bottom_left:

            st.subheader("📈 Average Sales")

            st.metric(
                "",
                f"${df['Sales'].mean():,.0f}"
            )

        with bottom_right:

            st.subheader("📄 Dataset Preview")

            st.dataframe(df.head())

        # =========================
        # DATE CONVERSION
        # =========================

        df['Order Date'] = pd.to_datetime(
            df['Order Date']
        )

        # Extract month
        df['Month'] = df['Order Date'].dt.month

        # Monthly sales
        monthly_sales = df.groupby(
            'Month'
        )['Sales'].sum().reset_index()

        # =========================
        # TRAIN MODEL
        # =========================

        X = monthly_sales[['Month']]
        y = monthly_sales['Sales']

        model = LinearRegression()

        model.fit(X, y)

        # Future months
        future_months = np.array(
            [[13], [14], [15]]
        )

        predictions = model.predict(
            future_months
        )

        # =========================
        # GRAPH
        # =========================

        st.subheader("📈 Sales Forecast Graph")

        fig, ax = plt.subplots(figsize=(10,5))

        ax.plot(
            monthly_sales['Month'],
            monthly_sales['Sales'],
            marker='o',
            label='Actual Sales'
        )

        ax.plot(
            [13,14,15],
            predictions,
            marker='o',
            linestyle='dashed',
            label='Predicted Sales'
        )

        ax.set_xlabel("Month")

        ax.set_ylabel("Sales")

        ax.set_title("Sales Forecast")

        ax.legend()

        ax.grid(True)

        st.pyplot(fig)

        # =========================
        # AI INSIGHT
        # =========================

        st.info(
            f"📈 AI predicts future sales may grow up to ${predictions[-1]:,.0f}"
        )

    except:

        st.error("❌ Please upload a valid CSV file")