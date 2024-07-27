# import joblib
# import pandas as pd

# def make_prediction(data: pd.DataFrame):
#     model = joblib.load("model.pkl")
#     prediction = model.predict(data)
#     return prediction.tolist()


from fastapi import HTTPException
import joblib
import pandas as pd
import os

# Dependency for preprocessing
def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    """Preprocess input data to match the training data."""
    data = data.copy()
    data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})
    data['Embarked'] = data['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})
    # Ensure all columns are present with the correct data types
    expected_columns = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
    for col in expected_columns:
        if col not in data.columns:
            data[col] = 0
    data = data[expected_columns]
    return data


# Dependency for loading the model
def get_model():
    if not os.path.exists("model.pkl"):
        raise HTTPException(status_code=400, detail="Model not trained yet")
    model = joblib.load("model.pkl")
    return model

def make_prediction(data: pd.DataFrame):
    model = joblib.load("model.pkl")
    processed_data = preprocess(data)
    prediction = model.predict(processed_data)
    return prediction.tolist()

