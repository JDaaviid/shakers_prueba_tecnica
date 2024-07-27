from pydantic import BaseModel

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
