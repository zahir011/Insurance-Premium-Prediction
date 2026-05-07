# Insurance Premium Prediction

A simple insurance premium prediction application built with FastAPI and Streamlit. This repository includes a REST API for model inference, a Streamlit user interface for submitting inputs, and a pre-trained machine learning model for predicting insurance premium categories.

## 🚀 Project Overview

The app predicts an insurance premium category based on user inputs such as age, weight, height, income, smoking status, city, and occupation.

The system consists of:
- `app.py`: FastAPI application exposing a `/predict` endpoint.
- `streamlit_app.py`: Streamlit frontend for users to enter details and receive predictions.
- `model/predict.py`: Prediction logic that loads a serialized model from `model/model.pkl`.
- `schema/`: Pydantic schemas for request validation and response formatting.

## 🔧 Key Features

- FastAPI REST endpoint for prediction
- Streamlit-based interactive UI
- BMI, lifestyle risk, age group, and city tier derivation
- Model prediction with class probabilities and confidence score
- Docker support for containerized deployment

## 📦 Requirements

Python dependencies are listed in `requirements.txt`.

Notable packages:
- `fastapi`
- `uvicorn`
- `streamlit`
- `pydantic`
- `scikit-learn`
- `pandas`
- `numpy`

## 🧩 Repository Structure

```text
app.py
streamlit_app.py
requirements.txt
dockerfile
model/
  ├── model.pkl
  └── predict.py
schema/
  ├── user_input.py
  ├── prediction_response.py
  └── config/
      └── city_tier.py
```

## 🛠️ Setup Instructions

### Option 1: Using the provided virtual environment

If you already have the repository's `myenv` virtual environment, activate it first.

Windows PowerShell:
```powershell
& .\myenv\Scripts\Activate.ps1
```

### Option 2: Create a new virtual environment

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## ▶️ Run the API

Start the FastAPI server:

```powershell
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Then visit the API docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## ▶️ Run the Streamlit App

In a new terminal, run:

```powershell
streamlit run streamlit_app.py
```

Open the URL shown in the terminal, usually `http://localhost:8501`.

> The Streamlit app sends prediction requests to `http://localhost:8000/predict`, so make sure the FastAPI server is running first.

## 🧪 API Usage

### POST `/predict`

Request body must include:
- `age`: int
- `weight`: float
- `height`: float
- `income_lpa`: float
- `smoker`: bool
- `city`: str
- `occupation`: str

Example JSON request:

```json
{
  "age": 35,
  "weight": 72.0,
  "height": 1.72,
  "income_lpa": 7.5,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

Example response:

```json
{
  "response": {
    "predicted_category": "High",
    "confidence": 0.842,
    "class_probabilities": {
      "Low": 0.03,
      "Medium": 0.13,
      "High": 0.84
    }
  }
}
```

## 🧠 Prediction Logic

The model uses derived user features:
- `bmi`: calculated from weight and height
- `lifestyle_risk`: determined by smoking status and BMI
- `age_group`: derived from age
- `city_tier`: determined from city membership in predefined tier lists

## 📦 Docker

Build the Docker image:

```powershell
docker build -t insurance-premium-predictor .
```

Run the container:

```powershell
docker run -p 8000:8000 insurance-premium-predictor
```

Then access the API at `http://localhost:8000`.

## 📝 Notes

- The app assumes the `model/model.pkl` file exists and is compatible with the current prediction pipeline.
- The Streamlit UI is configured to work with the local FastAPI server on port `8000`.

## 📁 Useful Files

- `app.py` — FastAPI server definition and routes
- `streamlit_app.py` — user interface for submitting data and displaying predictions
- `model/predict.py` — model loading and prediction helper
- `schema/user_input.py` — request validation and feature derivation
- `schema/prediction_response.py` — response schema for prediction output

## 💡 Suggestions

- Add a README section describing the model training process if you want to make this repo more complete.
- Add tests for the API and prediction pipeline for production reliability.
- Add a `requirements-dev.txt` for development-only dependencies.
