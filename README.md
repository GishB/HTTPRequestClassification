# HTTP Request Classification
- This project has been created as a result of test for Machine Learning engineer position at "Secret".

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Here you see an example how you can classify different HTTP requests.

In short main idea is to get features from HTTP requests then transform it via en encoder and predict class of an HTTP request via simple Decision Tree.

## How it works?
1. Extract features from raw data
2. Compress the features to an representation with shape (10,)
3. Make classification based the compressed data.
4. Send results back in json format like [{"EVENT_ID":"Ax001", "LABEL_PRED": 1}]

## What models are used for this results?
For raw data extraction task has been used custom class in utils dir. To compress data has been used custom MLPAutoEncoder (reduce shape from 42 to 10 values). To set up initial labels has been used OPTICS model from scikit-learn. After that all data has been trained with CatBoostClassifier.

## What results models have?
Here we have about 50 classes of HTTP request. From -1 to 48.

For CatBoostClassifier over 50 classes results show over 93% accuracy.

![image](https://github.com/GishB/PositiveTechnologiesTest/assets/90556084/413cb47e-34b2-4620-a578-70693fd9c3ce)

For custom MLPAutoEncoder result shows less ~0.01 MSE for enoding-decoding features after 100 epochs.

![image](https://github.com/GishB/PositiveTechnologiesTest/assets/90556084/5b23ac87-9951-498c-a001-810fc6b10509)


## There is any logical in classification labels?
It seems that OPTICS setup labels quite well.

For example class 27 for bot HTTP request:

![image](https://github.com/GishB/PositiveTechnologiesTest/assets/90556084/cfbb84c6-bd86-4390-94f9-c2881b3bd758)


For example class 19 which seems to be a danger HTTP request.

![image](https://github.com/GishB/PositiveTechnologiesTest/assets/90556084/600430d4-3f43-458d-aa20-d1a44daba629)




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

