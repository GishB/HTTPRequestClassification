# PositiveTechnologiesTest
An example how to classify different HTTP request.

## 1. If you running main.py localy.

  a) cd ./app
  
  b) python3 main.py

### Your server will be available here: ip=127.0.0.1, port=8127.

To test fastapi app for classification task >> Type next code in your terminal:

    curl -X 'POST' 'http://127.0.0.1:8127/predict' -H 'accept: application/json' -H 'Content-Type: application/json' -d '[
          {
            "CLIENT_IP": "188.138.92.55",
            "EVENT_ID": "AVdhXFgVq1Ppo9zF5Fxu",
            "CLIENT_USERAGENT": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
            "REQUEST_SIZE": 166,
            "RESPONSE_CODE": 404,
            "MATCHED_VARIABLE_SRC": "REQUEST_URI",
            "MATCHED_VARIABLE_NAME": "url",
            "MATCHED_VARIABLE_VALUE": "//tmp/20160925122692indo.php.vob"
          }
        ]'


## 2. If you running with docker.
  ...
  
