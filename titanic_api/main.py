from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from train import train_model
from predict import make_prediction, preprocess, get_model
import pandas as pd
from typing import List

app = FastAPI()

class TrainRequest(BaseModel):
    test_size: float

class PredictRequest(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str

@app.post("/train")
async def train(request: TrainRequest, background_tasks: BackgroundTasks):
    """Start training in the background."""
    background_tasks.add_task(train_model, request.test_size)
    return {"message": "Training started in background"}

@app.post("/predict")
async def predict(predict_request: PredictRequest,  model = Depends(get_model)):
    """Predict the survival for the provided data."""
    try:
        # data = pd.DataFrame([request.dict()])
        # prediction = make_prediction(data)
        # return {"prediction": prediction}
    
        print("PREDICT Request: ", predict_request.model_dump())    
        data = pd.DataFrame([predict_request.model_dump()])
        processed_data = preprocess(data)
        prediction = model.predict(processed_data)
        return {"prediction": prediction.tolist()}
        
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
