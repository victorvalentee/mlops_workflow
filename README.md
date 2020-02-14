# iFood MLOps Engineer Test

This repository holds all necessary code and instructions to run an **automated Machine Learning classification worflow** on the [Breast Cancer Winsconsin Diagnostics Dataset](https://www.kaggle.com/uciml/breast-cancer-wisconsin-data).

This dataset represents a series of patient tumor data and their diagnostics (M = malignant, B = benign), and our automated workflow contains the following steps:
- data ingestion
- model training, testing and evaluation
- model persistence (saving on disk)
- model serving via Flask API

## The Workflow
The workflow is divided in three parts:
1. `training/model_building.py`, responsible for data ingestion, model buiding and model persistence.
2. `api/app.py`, responsible for loading and setting up the API in which the model will be served.
3. `start.sh`, a shell script responsible for setting up the container environment and orchestrating the workflow.

## The API

Click [here](https://app.swaggerhub.com/apis/victorvalentee/iFoodMLTestAPI/0.1.0) for this API's full Swagger documentation. It's a very simple API with a POST endpoint that a client can make requests to.

Request body example:
```json
"mean radius": 1.0,
"mean texture": 2.0,
"mean perimeter": 3.0
```

Response example:
`"M"` or `"B"`.

## How to run

Clone this repo:

You can run it on Docker!

Using a terminal, go on the root folder where the Dockerfile is located and run:

```
$ sudo docker image build -t "ml_workflow" .
$ sudo docker run -it -p 5000:5000 ml_workflow /bin/bash
```

These commands will build a docker image and run a docker container that has our ML workflow application, and all the steps described in the previous section will run automatically.

**After a few seconds, you can already send requests to the API** using curl, swagger, postman or your prefered API testing tool. And you can do this from inside the container or on your localhost.