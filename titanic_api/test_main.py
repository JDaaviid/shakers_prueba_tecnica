from fastapi.testclient import TestClient
from main import app
import time
import os

client = TestClient(app)

def train_model():
    """Helper function to call the training API endpoint."""
    response = client.post("/train", json={"test_size": 0.2})
    assert response.status_code == 200
    assert response.json() == {"message": "Training started in background"}


def test_predict_endpoint():

    response = client.post("/predict", json={
        "Pclass": 3,
        "Sex": "male",
        "Age": 22.0,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 7.25,
        "Embarked": "S"
    })

    print("Prediction request status code:", response.status_code)
    print("Prediction request response:", response.json())
    
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_predict_invalid_input():
    response = client.post("/predict", json={
        "Pclass": "invalid",
        "Sex": "male",
        "Age": 22.0,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 7.25,
        "Embarked": "S"
    })
    print("Invalid input request status code:", response.status_code)
    print("Invalid input request response:", response.json())
    
    assert response.status_code == 422 

# Call the train API and run tests when the script is run directly
if __name__ == "__main__":
    print("Starting tests...")
    train_model()
    #wait_for_training_completion()
    print("Training completed. Running tests...")
    #test_train_endpoint()
    test_predict_endpoint()
    test_predict_invalid_input()
    print("All tests completed.")
