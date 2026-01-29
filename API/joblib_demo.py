import joblib
joblib.dump(model_pipeline, "loan_pretrained.pkl")
 
from flask import Flask, jsonify, request, render_template
import pandas as pd
 
app = Flask(__name__)
 
model_pipeline_loaded = joblib.load("loan_pretrained.pkl")
 
@app.route("/predict", methods=["POST"])
def predict():
 
    data = request.get_json()
    df= pd.DataFrame(data, index=[0])
    prediction = model_pipeline_loaded.predict(df)
    print(prediction)
    return jsonify({       
        "predicted_output": int(prediction[0])
    })
app.run(port=5000, debug=False, use_reloader=False)
 
if __name__ == '__main__':
    app.run(debug=True)