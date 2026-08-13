
from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os
from io import StringIO

# Create the Flask application
app = Flask(__name__)

# Locate the directory containing this app.py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the path to the serialized model
model_path = os.path.join(
    BASE_DIR,
    "sales_forecast_prediction_model_v1_0.joblib"
)

# Load the trained preprocessing + XGBoost pipeline
model = joblib.load(model_path)


# Basic route to confirm the API is running
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "SuperKart Sales Forecast Prediction API is running."
    })


# Prediction endpoint
@app.route("/predict", methods=["POST"])
def predict():

    # Read JSON sent to the API
    input_data = request.get_json()

    # Expected model features
    required_features = [
        "Product_Weight",
        "Product_Sugar_Content",
        "Product_Allocated_Area",
        "Product_Type",
        "Product_MRP",
        "Store_Establishment_Year",
        "Store_Size",
        "Store_Location_City_Type",
        "Store_Type"
    ]

    # Make sure all required fields were supplied
    missing_features = [
        feature for feature in required_features
        if feature not in input_data
    ]

    if missing_features:
        return jsonify({
            "error": "Missing required features",
            "missing_features": missing_features
        }), 400

    # Convert the incoming record into a one-row DataFrame
    input_df = pd.DataFrame(
        [input_data],
        columns=required_features
    )

    # Generate prediction
    prediction = model.predict(input_df)[0]

    # Return prediction as JSON
    return jsonify({
        "predicted_sales_revenue": float(prediction)
    })

@app.route("/batch_predict", methods=["POST"])
def batch_predict():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        batch_df = pd.read_csv(file)

        required_features = [
            "Product_Weight",
            "Product_Sugar_Content",
            "Product_Allocated_Area",
            "Product_Type",
            "Product_MRP",
            "Store_Establishment_Year",
            "Store_Size",
            "Store_Location_City_Type",
            "Store_Type"
        ]

        missing_features = [
            feature for feature in required_features
            if feature not in batch_df.columns
        ]

        if missing_features:
            return jsonify({
                "error": "Missing required features",
                "missing_features": missing_features
            }), 400

        # Keep only the model input columns
        prediction_df = batch_df[required_features].copy()

        # Generate predictions
        predictions = model.predict(prediction_df)

        # Add predictions to uploaded data
        batch_df["Predicted_Sales_Revenue"] = predictions

        return batch_df.to_json(
            orient="records"
        )

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7860
    )
