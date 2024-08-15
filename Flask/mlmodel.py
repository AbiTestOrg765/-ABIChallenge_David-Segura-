import pandas as pd
import pickle
import warnings
import json
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from .preprocess import pre
warnings.filterwarnings("ignore")
def predict(new_passengers):
    number_new_passengers = len(new_passengers)
    with open('Titanic_pipeline_model_nopre.pkl', 'rb') as f:
        loaded_pipeline = pickle.load(f)

        test = pd.read_csv('test.csv')

    new_preprocessor = FunctionTransformer(pre, validate=False)

    new_pipeline = Pipeline([
        ('preprocessor', new_preprocessor),
        ('classifier', loaded_pipeline.named_steps['classifier'])
    ], memory= None)
    
    new_passengers_df = pd.DataFrame(new_passengers)
    new_passengers_df['PassengerId'] = range(1310, 1310 + len(new_passengers_df))
    new_passengers_df['Fare'] = pd.to_numeric(new_passengers_df['Fare'], errors='coerce')
    new_passengers_df['Age'] = pd.to_numeric(new_passengers_df['Age'], errors='coerce')
    new_test = pd.concat([test, new_passengers_df], ignore_index=True)

    preds = new_pipeline.predict(new_test)
    ids = new_test['PassengerId']

    prediction_df = pd.DataFrame({'PassengerId' : ids, 'Survived' : preds})

    last_five = prediction_df.tail(number_new_passengers)
    last_five_dict = last_five.to_dict('records')
    json_data = json.dumps(last_five_dict)
    return json_data