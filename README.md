# PositiveTechnologiesTest
An example how to classify different HTTP request.

## 1. If you running main.py localy.
a) Go to app directory.

    cd ./app
  
b) Run via python3 file main.py where all configs are defined.

    python3 main.py

### App will be available here: ip=127.0.0.1, port=8127.

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

To check that app is available localy:

    curl -X 'GET' 'http://127.0.0.1:8127/' 



## 2. If you running with docker.
a) Create application image.
    
    sudo docker build -t classification_http:baseline .

b) Run the image 

    sudo docker run -d --name test -p 8127:80 classification_http:baseline
    
### App will be available here: ip=0.0.0.0, port=8127
To test fastapi in docker container you have to use next curl example:


    curl -X 'POST' 'http://0.0.0.0:8127/predict' -H 'accept: application/json' -H 'Content-Type: application/json' -d '[
          {
            "CLIENT_IP": "188.138.92.55",
            "EVENT_ID": "AVdhXFgVq1Ppo9zF5Fxu",
            "CLIENT_USERAGENT": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
            "REQUEST_SIZE": 166,
            "RESPONSE_CODE": 404,
            "MATCHED_VARIABLE_SRC": "REQUEST_URI",
            "MATCHED_VARIABLE_NAME": "url",
            "MATCHED_VARIABLE_VALUE": "//tmp/20160925122692indo.php.vob"
          },
          {
            "CLIENT_IP": "127.0.0.1",
            "EVENT_ID": "CustomEVENTID001",
            "CLIENT_USERAGENT": "select user_name from table",
            "REQUEST_SIZE": 2000,
            "RESPONSE_CODE": 200,
            "MATCHED_VARIABLE_SRC": "REQUEST_GET_ARGS",
            "MATCHED_VARIABLE_NAME": "REQUEST_GET_ARGS._",
            "MATCHED_VARIABLE_VALUE": "Aleksandr Samofalov"
          }
        ]'

![image](https://github.com/GishB/PositiveTechnologiesTest/assets/90556084/bae8c00d-e82b-4a5e-94e8-8d5c23233f63)


To check that app is available inside container:

    curl -X 'GET' 'http://0.0.0.0:8127/' 

![image](https://github.com/GishB/PositiveTechnologiesTest/assets/90556084/249ae5f7-bd6d-40d0-ac50-b339bf0ef786)

