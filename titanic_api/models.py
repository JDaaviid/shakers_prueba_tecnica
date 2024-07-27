from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

from database import Base

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

class Passenger(Base):
    __tablename__ = "passengers"
    id = Column(Integer, primary_key=True, index=True)
    #PassengerId = Column(Integer, unique=True, index=True)
    #Survived = Column(Integer)
    Pclass = Column(Integer)
    #Name = Column(String(255))
    Sex = Column(String(6))
    Age = Column(Float)
    SibSp = Column(Integer)
    Parch = Column(Integer)
    #Ticket = Column(String(20))
    Fare = Column(Float)
    #Cabin = Column(String(20))
    Embarked = Column(String(1))

