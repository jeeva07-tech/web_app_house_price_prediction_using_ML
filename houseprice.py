import pandas as pd
import streamlit as st
import joblib

# Load Model with Error Handling
try:
    model = joblib.load('xgb_model.jb')
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Background Image and Styling Fix
st.markdown(
    """
    <style>
        .stApp {
            background: url('https://source.unsplash.com/1600x900/?house') no-repeat center center fixed;
            background-size: cover;
        }
        .card {
            background: rgba(255, 255, 255, 0.85);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            margin: 20px;
        }
        h1 {
            color: #003366;
            text-align: center;
        }
        .stButton>button {
            background-color: #FF5733 !important;
            color: white !important;
            font-size: 18px !important;
            border-radius: 8px !important;
            width: 100% !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Title
st.markdown('<h1>🏡 House Price Prediction</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:18px; color:#444;">Enter the details below to predict the house price.</p>', unsafe_allow_html=True)

# Input Features
inputs = [
    'OverallQual', 'GrLivArea', 'GarageArea', '1stFlrSF',
    'FullBathroom', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'Fireplaces',
    'BsmtFinSF1', 'LotFrontage', 'WoodDeckSF', 'OpenPorchSF', 'LotArea',
    'CentralAir'
]

# Add a styled card container
st.markdown('<div class="card">', unsafe_allow_html=True)

input_data = {}
for feature in inputs:
    if feature == 'CentralAir':
        input_data[feature] = st.selectbox(f"🔹 {feature}", options=['Yes', 'No'], index=0)
    else:
        input_data[feature] = st.number_input(
            f"🔹 {feature}",
            value=0.0,
            step=1.0 if feature in ['OverallQual', 'FullBath', 'Fireplaces'] else 0.1
        )

st.markdown('</div>', unsafe_allow_html=True)  # Close styled div

# Predict Button
if st.button("🔍 Predict Price"):
    input_data['CentralAir'] = 1 if input_data['CentralAir'] == "Yes" else 0
    input_df = pd.DataFrame([input_data])

    try:
        predictions = model.predict(input_df)
        st.markdown(f'<p style="text-align:center; font-size:22px; color:#008000;"><b>🏠 Predicted House Price: ${predictions[0]:,.2f}</b></p>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Prediction Error: {e}")
