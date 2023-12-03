import sys
import uvicorn
from typing import List
from fastapi import FastAPI

sys.path.append("..")

from info.schema import HTTPRequestItem, PredictionResultItem
from utils.ModelUsagePiplines import get_prediction_results

app = FastAPI()


@app.get("/")
def say_hello():
    """ Check simple connections with FastAPI.

    Return:
        A simple string text from server.
    """
    return "Hello from server!"


@app.post("/predict", response_model=List[PredictionResultItem])
def predict(data: List[HTTPRequestItem]):
    """ Predict method via FastAPI.
    Arg:
        data: List of json data with HTTP requests.
    Note:
        This is an example function which helps to get prediction for a list of data.
    Return:

    """
    predictions: List[PredictionResultItem] = get_prediction_results(data)
    return predictions


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="127.0.0.1", port=8127, reload=True)
