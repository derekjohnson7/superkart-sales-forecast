# SuperKart Sales Forecasting

SuperKart is a retail chain operating supermarkets and food marts across multiple city tiers. This project develops and deploys a machine learning solution to forecast outlet sales revenue using historical product and store data.

The final solution uses a tuned XGBoost regression model wrapped in a preprocessing pipeline and deployed as a REST API. A Streamlit frontend provides both individual and batch prediction capabilities.

## Project Objective

The goal of this project is to build a forecasting solution that can support:

* Inventory planning
* Store-level sales forecasting
* Regional sales strategy
* Product and outlet scenario analysis
* Batch forecasting across multiple product/store combinations

## Model Development

Several regression approaches were evaluated, including:

* Decision Tree Regressor
* Tuned Decision Tree Regressor
* XGBoost Regressor
* Tuned XGBoost Regressor

The tuned XGBoost model was selected as the final model based on its overall performance on unseen test data.

### Final Model Performance

| Metric    | Tuned XGBoost |
| --------- | ------------: |
| Test RMSE |        285.87 |
| Test MAE  |        121.14 |
| Test R²   |        0.9284 |
| Test MAPE |         4.47% |

RMSE was used as the primary model-selection metric because it measures prediction error in the same units as the target variable while applying a greater penalty to larger forecasting errors.

## Features

The deployed model uses the following inputs:

* `Product_Weight`
* `Product_Sugar_Content`
* `Product_Allocated_Area`
* `Product_Type`
* `Product_MRP`
* `Store_Establishment_Year`
* `Store_Size`
* `Store_Location_City_Type`
* `Store_Type`

`Product_Id` and `Store_Id` were excluded from the final model because they function primarily as identifiers and provide limited generalizability for deployment across the broader store network.

## Preprocessing

The preprocessing pipeline includes:

* Median imputation for numerical features
* Most-frequent imputation for categorical features
* One-hot encoding for categorical variables
* Handling of previously unseen categorical values

The preprocessing pipeline and tuned XGBoost estimator are serialized together using `joblib` so the same transformations used during training are applied during inference.

## Application Architecture

```text
User
  ↓
Streamlit Frontend
  ↓
HTTP Request
  ↓
Render Backend Service
  ↓
Docker Container
  ↓
Gunicorn
  ↓
Flask REST API
  ↓
Serialized Preprocessing + XGBoost Pipeline
  ↓
Prediction
```

The backend and frontend are deployed as separate Dockerized services.

## Backend

The Flask backend exposes endpoints for both individual and batch predictions.

### Individual Prediction

`POST /predict`

Example request:

```json
{
  "Product_Weight": 12.53,
  "Product_Sugar_Content": "Regular",
  "Product_Allocated_Area": 0.066,
  "Product_Type": "Snack Foods",
  "Product_MRP": 145.62,
  "Store_Establishment_Year": 2009,
  "Store_Size": "Medium",
  "Store_Location_City_Type": "Tier 2",
  "Store_Type": "Supermarket Type2"
}
```

Example response:

```json
{
  "predicted_sales_revenue": 3466.14404296875
}
```

### Batch Prediction

`POST /batch_predict`

The batch endpoint accepts a CSV containing the required model features and returns predictions for all submitted rows.

## Streamlit Frontend

The Streamlit application provides:

* Interactive single-record forecasting
* Product and store input controls
* CSV upload for batch predictions
* Batch prediction preview
* Downloadable prediction results

## Repository Structure

```text
superkart-sales-forecast/
├── app.py
├── Dockerfile
├── requirements.txt
├── sales_forecast_prediction_model_v1_0.joblib
├── frontend/
│   ├── streamlit_app.py
│   ├── Dockerfile
│   └── requirements.txt
└── README.md
```

## Deployment

Both services are containerized using Docker and hosted on Render.

The backend is served using Gunicorn, which acts as the production WSGI server for the Flask application.

```text
Docker → Gunicorn → Flask → XGBoost
```

The Streamlit frontend communicates with the backend through HTTP requests.

### Live Backend

`https://superkart-sales-forecast.onrender.com/`

## Deployment Notes

The original project workflow used Hugging Face Docker Spaces. Due to changes in Hugging Face hosting requirements, Render was used as an alternative Docker hosting platform.

During deployment, package versions were pinned to match the model-training environment. This was necessary because serialized scikit-learn pipelines can depend on the library versions used when the model was created.

## Validation

The deployed API was validated against the locally trained model.

* Individual predictions from the deployed API matched local model predictions.
* Batch predictions were tested using observations from the test dataset.
* After standardizing the inputs supplied to both environments, deployed batch predictions matched local XGBoost predictions.

This confirms that the deployed preprocessing and inference pipeline behaves consistently with the development environment.

## Technologies Used

* Python
* pandas
* scikit-learn
* XGBoost
* Flask
* Gunicorn
* Streamlit
* Docker
* Render
* GitHub
* joblib

## Future Improvements

Potential future enhancements include:

* Automated model retraining
* Prediction monitoring and drift detection
* Authentication for API access
* Improved frontend validation
* Historical forecast tracking
* Feature importance and explainability views
* Integration with inventory planning systems
