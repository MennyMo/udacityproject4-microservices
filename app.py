from flask import Flask, request, jsonify, render_template
from flask.logging import create_logger
from forms import PredictionForm
import logging

import pandas as pd
#import joblib
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
app.config['SECRET_KEY'] = '03a78cc91ff590cd25450b394a5a9633'
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

def scale(payload):
    """Scales Payload"""
    
    LOG.info(f"Scaling Payload: \n{payload}")
    scaler = StandardScaler().fit(payload.astype(float))
    scaled_adhoc_predict = scaler.transform(payload.astype(float))
    return scaled_adhoc_predict

@app.route("/")
def home():
    return render_template('home.html')
    # html = f"<h3>Sklearn Prediction Home</h3>"
    # return html.format(format)

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    """Performs an sklearn prediction
        
        input looks like:
        {
        "CHAS":{
        "0":0
        },
        "RM":{
        "0":6.575
        },
        "TAX":{
        "0":296.0
        },
        "PTRATIO":{
        "0":15.3
        },
        "B":{
        "0":396.9
        },
        "LSTAT":{
        "0":4.98
        }
        
        result looks like:
        { "prediction": [ <val> ] }
        
        """
    
    # Logging the input payload
    json_payload = request.json
    LOG.info(f"JSON payload: \n{json_payload}")
    inference_payload = pd.DataFrame(json_payload)
    LOG.info(f"Inference payload DataFrame: \n{inference_payload}")
    # scale the input
    scaled_payload = scale(inference_payload)
    # get an output prediction from the pretrained model, clf
    prediction = list(clf.predict(scaled_payload))
    # TO DO:  Log the output prediction value
    LOG.info(f"output prediction: \n{prediction}")
    return jsonify({'prediction': prediction})

@app.route("/prediction", methods=['GET', 'POST'])
def predict_with_form():
    form = PredictionForm()
    if request.method == 'POST':
        CHAS = request.form.get('CHAS')
        RM = request.form.get('RM')
        TAX = request.form.get('TAX')
        PTRATIO = request.form.get('PTRATIO')
        B = request.form.get('B')
        LSTAT = request.form.get('LSTAT')

        newPayload = {
            'CHAS': {"0":CHAS},
            'RM': {"0":RM},
            'TAX': {"0":TAX},
            'PTRATIO': {"0":PTRATIO},
            'B': {"0":B},
            'LSTAT':{"0":LSTAT}
        }

        LOG.info(f"JSON payload: \n{newPayload}")
        inference_payload = pd.DataFrame(newPayload)
        LOG.info(f"Inference payload DataFrame: \n{inference_payload}")
        # scale the input
        scaled_payload = scale(inference_payload)
        # get an output prediction from the pretrained model, clf
        prediction = list(clf.predict(scaled_payload))
        # TO DO:  Log the output prediction value
        LOG.info(f"output prediction: {prediction}")
        return jsonify({'prediction': prediction})

    return render_template('predict.html', form=form)


if __name__ == "__main__":
    # load pretrained model as clf
    clf = joblib.load("./model_data/boston_housing_prediction.joblib")
    app.run(host='0.0.0.0', port=80, debug=True) # specify port=80


