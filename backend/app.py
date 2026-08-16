
import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# ---------------------------------------------------------
# Initialize Flask application
# ---------------------------------------------------------
superkart_api = Flask("SuperKart")


# ---------------------------------------------------------
# Load the trained model
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "superkart_model.joblib"
)

model = joblib.load(MODEL_PATH)


# ---------------------------------------------------------
# Features expected by the trained model
# ---------------------------------------------------------
FEATURES = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_Type",
    "Product_MRP",
    "Store_Id",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_Prefix",
    "Store_Age"
]


# ---------------------------------------------------------
# Home / health check
# ---------------------------------------------------------
@superkart_api.get("/")
def home():
    return jsonify(
        {
            "message": "Welcome to the SuperKart Sales Forecasting API",
            "status": "running"
        }
    )


# ---------------------------------------------------------
# Single prediction endpoint
# ---------------------------------------------------------
@superkart_api.post("/v1/predict")
def predict_sales():

    try:

        # Get JSON request data
        data = request.get_json()

        # Check that JSON data was received
        if not data:
            return jsonify(
                {
                    "error": "No JSON data received"
                }
            ), 400


        # Check for missing required features
        missing_features = [
            feature
            for feature in FEATURES
            if feature not in data
        ]

        if missing_features:
            return jsonify(
                {
                    "error": "Missing required features",
                    "missing_features": missing_features
                }
            ), 400


        # Create input dictionary in the correct feature order
        sample = {
            feature: data[feature]
            for feature in FEATURES
        }


        # Convert to DataFrame
        input_data = pd.DataFrame([sample])


        # Make prediction
        prediction = model.predict(input_data)[0]


        # Return result
        return jsonify(
            {
                "Sales": round(float(prediction), 2)
            }
        )


    except Exception as e:

        return jsonify(
            {
                "error": str(e)
            }
        ), 400


# ---------------------------------------------------------
# Batch prediction endpoint
# ---------------------------------------------------------
@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():

    try:

        # Check if file was uploaded
        if "file" not in request.files:

            return jsonify(
                {
                    "error": "No CSV file uploaded"
                }
            ), 400


        file = request.files["file"]


        # Check filename
        if file.filename == "":

            return jsonify(
                {
                    "error": "No file selected"
                }
            ), 400


        # Read uploaded CSV
        input_data = pd.read_csv(file)


        # Check for missing columns
        missing_features = [
            feature
            for feature in FEATURES
            if feature not in input_data.columns
        ]

        if missing_features:

            return jsonify(
                {
                    "error": "Missing required columns",
                    "missing_features": missing_features
                }
            ), 400


        # Keep only required features
        # and preserve the training feature order
        input_data = input_data[FEATURES]


        # Generate predictions
        predictions = model.predict(input_data)


        # Create output dictionary
        output_dict = {
            str(i): round(float(pred), 2)
            for i, pred in enumerate(predictions)
        }


        return jsonify(output_dict)


    except Exception as e:

        return jsonify(
            {
                "error": str(e)
            }
        ), 400


# ---------------------------------------------------------
# Run Flask application
# ---------------------------------------------------------
if __name__ == "__main__":
  superkart_api.run(debug=True)
