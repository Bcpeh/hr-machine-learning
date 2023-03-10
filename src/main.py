import joblib
from fastapi import FastAPI
from src.model.models import InputData
from src.config import APP_NAME, SWAGGER_ENDPOINT
from src.utils import preprocess, postprocess
import pandas as pd

tags_metadata = [{"name": "healthcheck"}, {"name": "model", "description": "Predicting variables"}]
app = FastAPI(title=APP_NAME, docs_url=SWAGGER_ENDPOINT, openapi_tags=tags_metadata)


# load the saved model from .pkl file
with open("src/model/grid.pkl", "rb") as f:
    model = joblib.load(f)


@app.get("/healthcheck", tags=["healthcheck"])
async def root():
    return {"message": "Hello World"}


# define your API endpoint
@app.post("/v1/predict", tags=["model"])
async def predict(input_data: InputData):
    # convert input data to the format expected by your model
    enrollee_id, input_data = preprocess(input_data)

    # make predictions using your model
    predictions = model.predict(input_data)

    # convert predictions to the format expected by the API response
    response = postprocess(enrollee_id, predictions)

    return response
