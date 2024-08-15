import pandas as pd
import pickle
import warnings
import json
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from .preprocess import pre
warnings.filterwarnings("ignore")
def predict(newPassengers):
    numberNewPassengers = len(newPassengers)
    with open('Titanic_pipeline_model_nopre.pkl', 'rb') as f:
        loaded_pipeline = pickle.load(f)

        test = pd.read_csv('test.csv')

    new_preprocessor = FunctionTransformer(pre, validate=False)

    new_pipeline = Pipeline([
        ('preprocessor', new_preprocessor),
        ('classifier', loaded_pipeline.named_steps['classifier'])
    ])
    
    newPassengers = pd.DataFrame(newPassengers)
    newPassengers['PassengerId'] = range(1310, 1310 + len(newPassengers))
    newPassengers['Fare'] = pd.to_numeric(newPassengers['Fare'], errors='coerce')
    newPassengers['Age'] = pd.to_numeric(newPassengers['Age'], errors='coerce')
    newTest = pd.concat([test, newPassengers], ignore_index=True)

    preds = new_pipeline.predict(newTest)
    ids = newTest['PassengerId']

    PredictionDF = pd.DataFrame({'PassengerId' : ids, 'Survived' : preds})

    last_five = PredictionDF.tail(numberNewPassengers)
    last_five_dict = last_five.to_dict('records')
    json_data = json.dumps(last_five_dict)
    return json_data