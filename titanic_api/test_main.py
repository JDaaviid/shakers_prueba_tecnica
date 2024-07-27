from fastapi.testclient import TestClient
from main import app
from models import Passenger
from database import SessionLocal


client = TestClient(app)


def load_passengers():
    csv_file_path = "dataset/train.csv"  # Update this path
    
    with open(csv_file_path, "rb") as f:
        response = client.post("/load-passengers/", files={"file": ("titanic.csv", f, "text/csv")})
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        assert response.status_code == 200
        assert response.json() == {"message": "Passengers loaded successfully"}


def train_model():
    """Helper function to call the training API endpoint."""
    headers = {"api-token": "1111"}  # Replace 'your_api_token_here' with the actual token value
    data = {"test_size": 0.2}  # Example payload, ensure this matches your TrainRequest model

    # Make the POST request to the /train/ endpoint
    response = client.post("/train", headers=headers, json=data)
    
    print(f"Train Model Response Status Code: {response.status_code}")
    print(f"Train Model Response Body: {response.text}")
    
    
    assert response.status_code == 200
    assert response.json() == {"message": "Training started in background"}


def test_predict_endpoint():
    
    headers = {"api-token": "1111"}  

    response = client.post("/predict", headers=headers, json={
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
    
    headers = {"api-token": "1111"}  
    
    response = client.post("/predict", headers=headers, json={
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
    
    
def test_add_passenger():
    """Test adding a passenger."""
    headers = {"api-token": "1111"}  
    
    passenger_data = {
        "Pclass": 1,
        "Sex": "female",  # Ensure this matches your schema's expected value
        "Age": 30.0,
        "SibSp": 0,
        "Parch": 0,
        "Fare": 50.0,
        "Embarked": "S"  
    }
    
    response = client.post("/add_passenger", json=passenger_data, headers=headers)
    
    print("Add passenger request status code:", response.status_code)
    print("Add passenger request response:", response.json())
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Passenger added"
    
    # Check the ID in the response and verify passenger in database
    passenger_id = response_data["passenger_id"]
    assert passenger_id is not None
    
    with SessionLocal() as session:
        added_passenger = session.query(Passenger).filter(Passenger.id == passenger_id).first()
        assert added_passenger is not None
        assert added_passenger.Pclass == passenger_data["Pclass"]
        assert added_passenger.Sex == passenger_data["Sex"]
        assert added_passenger.Age == passenger_data["Age"]
        assert added_passenger.SibSp == passenger_data["SibSp"]
        assert added_passenger.Parch == passenger_data["Parch"]
        assert added_passenger.Fare == passenger_data["Fare"]
        assert added_passenger.Embarked == passenger_data["Embarked"]

# Call the train API and run tests when the script is run directly
if __name__ == "__main__":
    print("Starting tests...")
    load_passengers()  # Load passengers into the database
    train_model()
    print("Training completed. Running tests...")
    #test_train_endpoint()
    test_predict_endpoint()
    test_predict_invalid_input()
    test_add_passenger()  
    print("All tests completed.")
