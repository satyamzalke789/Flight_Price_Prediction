import streamlit as st
import pandas as pd
import joblib

# =============================
# ✅ Must be the first Streamlit command
# =============================
st.set_page_config(page_title="Flight Price Predictor", page_icon="✈️")

# =============================
# Load trained RandomForest model
# =============================
MODEL_PATH = "best_flight_price_model_RandomForest.pkl"  # update if filename differs
model = joblib.load(MODEL_PATH)

# =============================
# Airline-Themed Styling
# =============================
page_style = """
<style>
/* Main App background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #87ceeb, #ffffff); /* Sky blue to white */
    background-attachment: fixed;
    font-family: 'Arial', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364); /* Dark airline blue */
    color: white;
}

/* Airplane watermark */
[data-testid="stAppViewContainer"]::before {
    content: "";
    background-image: url("https://cdn-icons-png.flaticon.com/512/681/681494.png");
    background-size: 180px;
    background-repeat: no-repeat;
    position: absolute;
    top: 25%;
    left: 70%;
    opacity: 0.08;
    height: 100%;
    width: 100%;
    pointer-events: none;
    z-index: 0;
}

/* Headers */
h1, h2, h3 {
    color: #0d47a1; /* Airline deep blue */
    font-weight: bold;
    text-shadow: 1px 1px 2px #ffffff;
}

/* Input widgets */
.stSelectbox, .stRadio, .stSlider, .stNumberInput {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 8px;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}

/* Buttons */
div.stButton > button {
    background-color: #0d47a1;
    color: white;
    border-radius: 12px;
    padding: 0.6em 1.2em;
    border: none;
    font-weight: bold;
    box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: #1976d2;
    transform: scale(1.05);
    cursor: pointer;
}

/* Success message */
.stAlert {
    border-radius: 10px;
    font-weight: bold;
}

/* Prediction output highlight */
[data-testid="stSuccess"] {
    background-color: #e3f2fd;
    color: #0d47a1;
    border: 2px solid #90caf9;
    border-radius: 12px;
    font-size: 1.1em;
    padding: 12px;
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# =============================
# Branded Top Banner
# =============================
st.markdown(
    """
    <div style="
        background: linear-gradient(to right, #0d47a1, #1976d2);
        padding: 15px 25px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    ">
        <img src="https://cdn-icons-png.flaticon.com/512/681/681494.png" 
             width="50" style="margin-right:15px;">
        <h1 style="color:white; margin:0; font-size:28px;">
            Airline Price Predictor ✈️
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# =============================
# Input Section
# =============================
st.write("Enter flight details to predict the price.")

airline = st.selectbox("Airline", ["SpiceJet", "AirAsia", "Vistara", "GO_FIRST", "Indigo", "Air_India"])
source_city = st.selectbox("Source City", ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai", "Hyderabad"])
destination_city = st.selectbox("Destination City", ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai", "Hyderabad"])
departure_time = st.selectbox("Departure Time", ["Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"])
arrival_time = st.selectbox("Arrival Time", ["Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"])
stops = st.selectbox("Number of Stops", ["zero", "one", "two_or_more"])
flight_class = st.radio("Class", ["Economy", "Business"])
duration = st.number_input("Duration (in hours)", min_value=0.5, max_value=15.0, step=0.1, value=2.5)
days_left = st.slider("Days Left Until Flight", 0, 60, 10)

# =============================
# Prediction
# =============================
if st.button("Predict Price"):
    input_data = pd.DataFrame([{
        "airline": airline,
        "source_city": source_city,
        "departure_time": departure_time,
        "stops": stops,
        "arrival_time": arrival_time,
        "destination_city": destination_city,
        "class": flight_class,
        "duration": duration,
        "days_left": days_left
    }])

    prediction = model.predict(input_data)[0]
    st.success(f"💰 Predicted Ticket Price: ₹{int(prediction):,}")
