
import streamlit as st
import requests

# Backend API endpoint
API_URL = "https://superkart-sales-forecast.onrender.com/predict"

st.title("SuperKart Sales Forecasting")
st.write(
    "Enter product and store information to forecast sales revenue."
)

# Product inputs
product_weight = st.number_input(
    "Product Weight",
    min_value=1.0,
    max_value=25.0,
    value=12.66,
    step=0.01
)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.000,
    max_value=0.5,
    value=0.056,
    step=0.001,
    format="%.3f"
)

product_type = st.selectbox(
    "Product Type",
    [
        "Fruits and Vegetables",
        "Snack Foods",
        "Frozen Foods",
        "Dairy",
        "Household",
        "Baking Goods",
        "Canned",
        "Health and Hygiene",
        "Meat",
        "Soft Drinks",
        "Breads",
        "Hard Drinks",
        "Others",
        "Starchy Foods",
        "Breakfast",
        "Seafood"
    ]
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=100.0
)

# Store inputs
store_establishment_year = st.number_input(
    "Store Establishment Year",
    min_value=1900,
    max_value=2100,
    value=2000,
    step=1
)

store_size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

store_city_type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Supermarket Type1",
        "Supermarket Type2",
        "Departmental Store",
        "Food Mart"
    ]
)

if st.button("Predict Sales Revenue"):

    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": product_allocated_area,
        "Product_Type": product_type,
        "Product_MRP": product_mrp,
        "Store_Establishment_Year": store_establishment_year,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_city_type,
        "Store_Type": store_type
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=90
        )

        if response.status_code == 200:
            prediction = response.json()["predicted_sales_revenue"]

            st.success(
                f"Predicted Sales Revenue: {prediction:,.2f}"
            )

        else:
            st.error(
                f"Prediction failed. Status code: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        st.error(f"Unable to connect to prediction API: {e}")
