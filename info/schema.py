from pydantic import BaseModel, Field
from typing import Any, List


class HTTPRequestItem(BaseModel):
    CLIENT_IP: str = Field(examples=["188.138.92.55"])
    EVENT_ID: str = Field(examples=["AVdhXFgVq1Ppo9zF5Fxu"])
    CLIENT_USERAGENT: str | None = Field(examples=["Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 "
                                                   "Firefox/45.0"])
    REQUEST_SIZE: float | int = Field(examples=[166])
    RESPONSE_CODE: int = Field(examples=[404])
    MATCHED_VARIABLE_SRC: Any = Field(examples=["REQUEST_URI"])
    MATCHED_VARIABLE_NAME: Any = Field(examples=["url"])
    MATCHED_VARIABLE_VALUE: Any = Field(examples=["//tmp/20160925122692indo.php.vob"])


class PredictionResultItem(BaseModel):
    EVENT_ID: str = Field(examples=["AVdhXFgVq1Ppo9zF5Fxu"])
    LABEL_PRED: int = Field(examples=[1])
