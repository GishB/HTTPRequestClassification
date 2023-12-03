import sys

sys.path.append("..")

from info.schema import HTTPRequestItem, PredictionResultItem
from typing import List, Any

import torch
import numpy as np
import pandas as pd


class DataTransformer:
    """Main idea here is to transform raw data into appropriate encoded dataset.
    """

    def __init__(self,
                 df: pd.DataFrame = None,
                 model: object = None):
        if df is None or model is None:
            raise IndexError('Dataframe or MLPAutoEncdoer hasn`t been defined')
        self.df = df.reset_index(drop=True)
        self.model = model

    def preprocess(self) -> pd.DataFrame:
        """ Apply preprocessing over dataset.

        Return:
            DataFrame which is expected for MLPAutoEncdoer model.
        """
        self.df['REQUEST_SIZE'] = self.df['REQUEST_SIZE'].apply(lambda x: int(x))
        self.df['HEADER_pattern'] = self.df["CLIENT_USERAGENT"].str.contains("([a-zA-Z]/[\d].*_*)").fillna(False)
        self.df['BOT_BOOL'] = self.df["CLIENT_USERAGENT"].apply(lambda row: False if type(row) is not str else
        False if 'bot' not in row.lower() else True).fillna(False)
        self.df['CURL_HEAD_BOOL'] = self.df['CLIENT_USERAGENT'].apply(lambda x: True if 'curl' in x.lower() else False)
        self.df['WGET_HEAD_BOOL'] = self.df['CLIENT_USERAGENT'].apply(lambda x: True if 'wget' in x.lower() else False)
        self.df['LENGTH_DISCRET_APP'] = self.df['CLIENT_USERAGENT'].apply \
            (lambda x: 'Anomaly TOP' if len(x.split()[0]) > 50
            else 'user_expected' if len(x.split()[0]) >= 9 else 'Anomaly MIN')
        self.df['SYMBOL_@'] = self.df['CLIENT_USERAGENT'].apply(lambda x: True if '@' in x.split(' ')[0] else False)
        self.df['LENGTH_OF_USER_AGENT_HEAD_likely'] = self.df['CLIENT_USERAGENT'].apply \
            (lambda x: True if len(x.split(' ')) >= 4 else False)
        self.df['windows_bool'] = self.df['CLIENT_USERAGENT'].apply(lambda x: True if 'windows' in x.lower() else False)
        self.df['linux_bool'] = self.df['CLIENT_USERAGENT'].apply(lambda x: True if 'linux' in x.lower() else False)
        self.df['iphone_bool'] = self.df['CLIENT_USERAGENT'].apply(lambda x: True if 'iphone' in x.lower() else False)
        self.df['ipad_bool'] = self.df['CLIENT_USERAGENT'].apply(lambda x: True if 'ipad' in x.lower() else False)
        self.df['compatible_bool'] = self.df['CLIENT_USERAGENT'].apply \
            (lambda x: True if 'compatible' in x.lower() else False)
        self.df['lognorm_mean_request_size'] = self.get_normalized_mean_for_request_type()
        self.df['CURRENT_REQUEST_SIZE_lognorm'] = self.get_current_request_size_lognorm()
        self.df['RESPONSE_CODE'] = self.df['RESPONSE_CODE'].apply(lambda x: int(str(x)[0]))
        self.df['test'] = self.df['MATCHED_VARIABLE_NAME'].apply \
            (lambda x: "number" if type(x) != str else "none" if x == None else x.split('.')[0])
        self.df["BOOL_URL_VALUE"] = self.df['test'].apply(lambda x: True if x == 'url' else False)
        self.df["BOOL_IS_ASCII_VALUE"] = self.df['test'].apply(lambda x: True if x.isascii() else False)
        self.df['normalized_len_variable_name'] = \
            ((self.df['test'].apply(lambda x: len(str(x)) if type(x) is float else len(x)) - 0)
             / (242 - 0)).round(2)

        df_response_code = self.get_dummies_response_code()
        df_matched_variable_src = self.get_matched_variable_src()
        df_length_discret = self.get_length_discret()

        self.df = self.df.drop(axis=0,
                               columns=['CLIENT_USERAGENT', 'REQUEST_SIZE', 'RESPONSE_CODE', 'MATCHED_VARIABLE_SRC',
                                        'MATCHED_VARIABLE_NAME', 'MATCHED_VARIABLE_VALUE', 'LENGTH_DISCRET_APP'])
        self.df = self.df.drop(axis=1, columns=['test'])
        self.df = pd.concat([self.df, df_matched_variable_src, df_response_code, df_length_discret], axis=1)

        expected_columns = ['HEADER_pattern', 'BOT_BOOL', 'CURL_HEAD_BOOL', 'WGET_HEAD_BOOL', 'SYMBOL_@',
                            'LENGTH_OF_USER_AGENT_HEAD_likely',
                            'windows_bool', 'linux_bool', 'iphone_bool', 'ipad_bool', 'compatible_bool',
                            'lognorm_mean_request_size', 'CURRENT_REQUEST_SIZE_lognorm',
                            'BOOL_URL_VALUE', 'BOOL_IS_ASCII_VALUE', 'normalized_len_variable_name',
                            'CLIENT_SESSION_ID', 'CLIENT_USERAGENT', 'REQUEST_ARGS',
                            'REQUEST_ARGS_KEYS', 'REQUEST_CONTENT_TYPE', 'REQUEST_COOKIES', 'REQUEST_FILES',
                            'REQUEST_GET_ARGS', 'REQUEST_HEADERS', 'REQUEST_JSON',
                            "REQUEST_METHOD\\';\\'REQUEST_CONTE", "REQUEST_METHOD\\';\\'REQUEST_HEADE", 'REQUEST_PATH',
                            'REQUEST_POST_ARGS', 'REQUEST_QUERY', 'REQUEST_URI',
                            "REQUEST_URI\\';\\'REQUEST_ARGS", 'REQUEST_XML', 'RESPONSE_BODY', 'RESPONSE_HEADERS', "2",
                            "3", "4", "5", 'Anomaly TOP', 'user_expected']
        return self.df[expected_columns]

    def get_normalized_mean_for_request_type(self) -> float:
        dict_of_normalized_data = {'CLIENT_IP': 0.03, 'CLIENT_SESSION_ID': 0.18,
                                   'CLIENT_USERAGENT': 0.1, 'REQUEST_ARGS': 0.59, 'REQUEST_ARGS_KEYS': 0.99,
                                   'REQUEST_CONTENT_TYPE': 0.0, 'REQUEST_COOKIES': 0.43, 'REQUEST_FILES': 0.97,
                                   'REQUEST_GET_ARGS': 0.35, 'REQUEST_HEADERS': 0.52, 'REQUEST_JSON': 0.81,
                                   "REQUEST_METHOD\\';\\'REQUEST_CONTE": 1.0,
                                   "REQUEST_METHOD\\';\\'REQUEST_HEADE": 0.29,
                                   'REQUEST_PATH': 0.48,
                                   'REQUEST_POST_ARGS': 0.93,
                                   'REQUEST_QUERY': 0.03, 'REQUEST_URI': 0.14, "REQUEST_URI\\';\\'REQUEST_ARGS": 0.11,
                                   'REQUEST_XML': 0.64, 'RESPONSE_BODY': 0.46, 'RESPONSE_HEADERS': 0.4}
        return dict_of_normalized_data.get(self.df['MATCHED_VARIABLE_SRC'].values[0])

    def get_current_request_size_lognorm(self) -> float:
        max_log_val_request_size = 10.6
        min_log_val_request_size = 5.72
        val = (np.log(self.df['REQUEST_SIZE']) - min_log_val_request_size) / (
                max_log_val_request_size - min_log_val_request_size)
        val = val.values[0]
        if val > 1:
            val = 1
        elif val < 0:
            val = 0
        else:
            val = val
        return round(val, 2)

    def get_dummies_response_code(self) -> pd.DataFrame:
        response_dict = {2: [1, 0, 0, 0], 3: [0, 1, 0, 0], 4: [0, 0, 1, 0], 5: [0, 0, 0, 1]}
        return pd.DataFrame(data=[response_dict.get(self.df['RESPONSE_CODE'].values[0])],
                            columns=['2', '3', '4', '5'])

    def get_matched_variable_src(self) -> pd.DataFrame:
        list_matched_variable = ['CLIENT_SESSION_ID', 'CLIENT_USERAGENT', 'REQUEST_ARGS', 'REQUEST_ARGS_KEYS',
                                 'REQUEST_CONTENT_TYPE', 'REQUEST_COOKIES',
                                 'REQUEST_FILES', 'REQUEST_GET_ARGS', 'REQUEST_HEADERS', 'REQUEST_JSON',
                                 "REQUEST_METHOD\\';\\'REQUEST_CONTE",
                                 "REQUEST_METHOD\\';\\'REQUEST_HEADE", 'REQUEST_PATH', 'REQUEST_POST_ARGS',
                                 'REQUEST_QUERY', 'REQUEST_URI',
                                 "REQUEST_URI\\';\\'REQUEST_ARGS", 'REQUEST_XML', 'RESPONSE_BODY', 'RESPONSE_HEADERS']
        df_matched_variable_src = self.df['MATCHED_VARIABLE_SRC'].values[0]
        list_val_matched_variable_src = []
        for val in list_matched_variable:
            if val == df_matched_variable_src:
                list_val_matched_variable_src.append(1)
            else:
                list_val_matched_variable_src.append(0)
        return pd.DataFrame(data=[list_val_matched_variable_src],
                            columns=list_matched_variable)

    def get_length_discret(self) -> pd.DataFrame:
        df_discret_length_app = self.df['LENGTH_DISCRET_APP'].values[0]
        list_discret_length_app = []
        for val in ['Anomaly TOP', 'user_expected']:
            if val == df_discret_length_app:
                list_discret_length_app.append(1)
            else:
                list_discret_length_app.append(0)
        return pd.DataFrame(data=[list_discret_length_app],
                            columns=['Anomaly TOP', 'user_expected'])

    @torch.inference_mode()
    def transform(self) -> torch.Tensor:
        self.model.eval()
        init_features = torch.Tensor(self.preprocess().to_numpy().astype(float)).unsqueeze(0)
        return self.model.encoder(init_features).view(10).numpy()


def json_to_raw_dataframe(data: List[HTTPRequestItem]) -> pd.DataFrame:
    columns: List[str] = ['CLIENT_IP', 'EVENT_ID', 'CLIENT_USERAGENT', 'REQUEST_SIZE',
                          'RESPONSE_CODE', 'MATCHED_VARIABLE_SRC', 'MATCHED_VARIABLE_NAME', 'MATCHED_VARIABLE_VALUE']
    list_of_df = []
    for row in data:
        data_temp: List[Any] = [row.CLIENT_IP, row.EVENT_ID, row.CLIENT_USERAGENT, row.REQUEST_SIZE,
                                row.RESPONSE_CODE, row.MATCHED_VARIABLE_SRC, row.MATCHED_VARIABLE_NAME,
                                row.MATCHED_VARIABLE_VALUE]
        list_of_df.append(pd.DataFrame(data=[data_temp], columns=columns))
    df = pd.concat(list_of_df)
    return df.reset_index(drop=True)


def prepaire_json_result(event_id: str, predicted_class: int) -> PredictionResultItem:
    return {"EVENT_ID": event_id, "LABEL_PRED": predicted_class}
