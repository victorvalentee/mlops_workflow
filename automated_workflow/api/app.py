import os
import joblib
import numpy as np
from flask import Flask, request, jsonify

BASE_PATH = '/usr/local/automated_workflow'
SAVED_MODELS_PATH = f'{BASE_PATH}/api/saved_models'

app = Flask(__name__)

def get_latest_model():
    filenames = os.listdir(SAVED_MODELS_PATH)
    filenames.sort()
    
    latest_model = filenames[-1]
    model = joblib.load(f'{SAVED_MODELS_PATH}/{latest_model}', 'r')
    return model

model = get_latest_model()
print("Loaded model: ", model)

@app.route('/predict',methods=['POST'])
def predict():
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = str(prediction[0])
    
    if output == "1":
        output = "Benign"
    else:
        output = "Malignant"
    
    return jsonify(output)

if __name__ == "__main__":
    print("Setting up API...")
    app.run(debug=True, host="0.0.0.0")