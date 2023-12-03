import sys
import torch
from catboost import CatBoostClassifier
import pandas as pd

sys.path.append("..")

from info.schema import HTTPRequestItem, PredictionResultItem
from typing import List
from utils.DataTransformers import json_to_raw_dataframe, DataTransformer, prepaire_json_result


def load_model(is_torch: bool = True) -> torch.nn.Module | CatBoostClassifier:
    if is_torch:
        model = torch.jit.load("../models/baseline_mlp_autoencdoer.pt")
    else:
        clf = CatBoostClassifier()
        model = clf.load_model("../models/catboost_accuracy_093_over50class.pkl")
    return model


def collect_list_of_json_results(predicted_list_of_classes: List[int],
                                 df: pd.DataFrame = None) -> List[PredictionResultItem]:
    results = []
    for ind, predicted_class in enumerate(predicted_list_of_classes):
        predicted_class = predicted_list_of_classes[ind]
        results.append(prepaire_json_result(event_id=df['EVENT_ID'].iloc[ind],
                                            predicted_class=predicted_class))
    return results


def get_prediction_results(data: List[HTTPRequestItem]) -> List[PredictionResultItem]:
    df: pd.DataFrame = json_to_raw_dataframe(data)
    encoded_list_of_df = [DataTransformer(df=df_row.to_frame().T, model=load_model(is_torch=True)).transform()
                          for ind, df_row in df.iterrows()]
    clf = load_model(is_torch=False)
    predicted_list_of_classes = [clf.predict(x)[0] for x in encoded_list_of_df]
    return collect_list_of_json_results(predicted_list_of_classes, df)
