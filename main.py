from fastapi import FastAPI
import joblib
import numpy as np
from sklearn.datasets import load_iris  # 추가
app = FastAPI()

# Load the trained model
model = joblib.load('model.joblib')

# Load the iris dataset
iris = load_iris()  # 추가

# root 
@app.get("/")
def read_root():
    return {"message": "Welcome to the ML Model API V3"}

@app.post("/predict/")
def predict(data: dict):
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)
    class_name = iris.target_names[prediction][0]
    return {"class": class_name}