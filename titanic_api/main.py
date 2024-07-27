from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, Header, File, UploadFile
import pandas as pd
import joblib
import os
from sqlalchemy.orm import Session
from models import Passenger, PredictRequest, TrainRequest
from train import train_model
from database import SessionLocal, engine, Base
from dotenv import load_dotenv


load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Create the database tables
Base.metadata.create_all(bind=engine)

session = SessionLocal()

# Clear all records from the passengers table
session.query(Passenger).delete()
session.commit()


# FastAPI instance
app = FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for loading the model
def get_model():
    if not os.path.exists("model.pkl"):
        raise HTTPException(status_code=400, detail="Model not trained yet")
    model = joblib.load("model.pkl")
    return model

# Dependency for preprocessing
def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    """Preprocess input data to match the training data."""
    data = data.copy()
    data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})
    data['Embarked'] = data['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})
    expected_columns = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
    for col in expected_columns:
        if col not in data.columns:
            data[col] = 0
    data = data[expected_columns]
    return data



@app.post("/load-passengers/")
async def load_passengers(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    

    # Handle NaN values by replacing them with default values
    df['Embarked'] = df['Embarked'].fillna('')  
    df = df.fillna({
        'Pclass': 0,
        'Name': 'Unknown',
        'Sex': 'Unknown',
        'Age': 0.0,
        'SibSp': 0,
        'Parch': 0,
        'Ticket': 'Unknown',
        'Fare': 0.0,
        'Embarked': 'Unknown'
    })

    # Convert DataFrame columns to appropriate data types
    df['Age'] = df['Age'].astype(float)
    df['Fare'] = df['Fare'].astype(float)
    df['Pclass'] = df['Pclass'].astype(int)
    df['SibSp'] = df['SibSp'].astype(int)
    df['Parch'] = df['Parch'].astype(int)

    with SessionLocal() as session:
        for _, row in df.iterrows():
            passenger = Passenger(
                id=row.get('PassengerId'),
                Pclass=row.get('Pclass'),
                #Name=row.get('Name'),
                Sex=row.get('Sex'),
                Age=row.get('Age'),
                SibSp=row.get('SibSp'),
                Parch=row.get('Parch'),
                #Ticket=row.get('Ticket'),
                Fare=row.get('Fare'),
                Embarked=row.get('Embarked')
            )
            session.add(passenger)
        session.commit()
    return {"message": "Passengers loaded successfully"}

@app.post("/train")
async def train_endpoint(train_request: TrainRequest, background_tasks: BackgroundTasks, api_token: str = Header(...)):
    """Start training in the background."""
    if api_token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API Token")
    background_tasks.add_task(train_model, train_request.test_size)
    return {"message": "Training started in background"}

@app.post("/predict")
async def predict_endpoint(predict_request: PredictRequest, model = Depends(get_model), api_token: str = Header(...)):
    """Predict the survival for the provided data."""
    if api_token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API Token")
    

    data = pd.DataFrame([predict_request.dict()])
    processed_data = preprocess(data)
    prediction = model.predict(processed_data)
    return {"prediction": prediction.tolist()}

@app.post("/add_passenger")
async def add_passenger(predict_request: PredictRequest, db: Session = Depends(get_db), api_token: str = Header(...)):
    """Add a new passenger to the database."""
    if api_token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API Token")

    passenger = Passenger(
        Pclass=predict_request.Pclass,
        Sex=predict_request.Sex,
        Age=predict_request.Age,
        SibSp=predict_request.SibSp,
        Parch=predict_request.Parch,
        Fare=predict_request.Fare,
        Embarked=predict_request.Embarked
    )
    db.add(passenger)
    db.commit()
    db.refresh(passenger)
    return {"message": "Passenger added", "passenger_id": passenger.id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
