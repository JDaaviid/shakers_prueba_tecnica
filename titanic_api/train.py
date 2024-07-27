import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pandas as pd
import joblib


def train_model(test_size: float):
    # Load dataset
    data = pd.read_csv('dataset/train.csv')

    # Preprocess data
    data = data[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 'Survived']]
    data.dropna(inplace=True)
    data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})
    data['Embarked'] = data['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})

    X = data.drop('Survived', axis=1)
    y = data['Survived']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # Log with MLflow
    with mlflow.start_run():
        mlflow.sklearn.log_model(model, "model")
        mlflow.log_param("test_size", test_size)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision_score(y_test, predictions))
        mlflow.log_metric("recall", recall_score(y_test, predictions))
        mlflow.log_metric("f1_score", f1_score(y_test, predictions))
       
        # Log confusion matrix
        conf_matrix = confusion_matrix(y_test, predictions)
        with open('confusion_matrix.txt', 'w') as f:
            f.write(str(conf_matrix))
        mlflow.log_artifact('confusion_matrix.txt')
        
    joblib.dump(model, "model.pkl")

    print(f"Model trained with accuracy: {accuracy}")
