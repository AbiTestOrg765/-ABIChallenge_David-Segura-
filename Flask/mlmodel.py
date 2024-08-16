import pandas as pd
import pickle
import warnings
import json
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from .preprocess import pre # Import pre processing function

warnings.filterwarnings("ignore")

class TitanicModel:
    def __init__(self):
        """
        Loads and creates the new pipeline to run the model
        """
        with open('Titanic_pipeline_model_nopre.pkl', 'rb') as f:
            # Loads the pickle object
            loaded_pipeline = pickle.load(f)
            # loads the test dataset
            self.test = pd.read_csv('test.csv')

        # Creates a new Pre processing part.
        new_preprocessor = FunctionTransformer(pre, validate=False)

        # Appends the classifier with the pre processing.
        self.new_pipeline = Pipeline([
            ('preprocessor', new_preprocessor),
            ('classifier', loaded_pipeline.named_steps['classifier'])
        ], memory= None)

    def predict(self, new_passengers):
        """ Prediction function receives a list of passengers an returns a list

            Args:
                new_passengers (array): List of passenger information

            Returns:
                predictions (array): List of predictions 
        """

        # Get the number of new passengers
        number_new_passengers = len(new_passengers)

        # Concatenates the new Passengers to the Test dataset
        #the prediction requires a big amount of passengers so this step is a way
        #to bypass that requirement.
        new_passengers_df = pd.DataFrame(new_passengers)
        new_passengers_df['PassengerId'] = range(1310, 1310 + len(new_passengers_df))
        new_passengers_df['Fare'] = pd.to_numeric(new_passengers_df['Fare'], errors='coerce')
        new_passengers_df['Age'] = pd.to_numeric(new_passengers_df['Age'], errors='coerce')
        new_test = pd.concat([self.test, new_passengers_df], ignore_index=True)

        # Runs the model
        preds = self.new_pipeline.predict(new_test)

        names = new_test['Name']
        prediction_df = pd.DataFrame({'Passenger Name' : names, 'Survived' : preds})

        # Only returns the predictions for the new passengers
        new_passengers_predictions = prediction_df.tail(number_new_passengers)
        new_passengers_dict = new_passengers_predictions.to_dict('records')
        json_data = json.dumps(new_passengers_dict)
        return json_data