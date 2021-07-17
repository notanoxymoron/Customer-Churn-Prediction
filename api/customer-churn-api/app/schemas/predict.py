from typing import Any, List, Optional

from classification_model.processing.validation import ChurnDataInputSchema
from pydantic import BaseModel


class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[float]]


class MultipleChurnDataInputs(BaseModel):
    inputs: List[ChurnDataInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "Contract": "Month-to-month",
                        "Dependents": "No",
                        "DeviceProtection": "No",
                        "gender": "Female",
                        "InternetService": "DSL",
                        "MonthlyCharges": 29.85,
                        "MultipleLines": "No phone service",
                        "OnlineBackup": "Yes",
                        "OnlineSecurity": "No",
                        "PaperlessBilling": "Yes",
                        "Partner": "Yes",
                        "PaymentMethod": "Electronic check",
                        "PhoneService": "No",
                        "SeniorCitizen": 0,
                        "StreamingMovies": "No",
                        "StreamingTV": "No",
                        "TechSupport": "No",
                        "tenure": 1,
                        "TotalCharges": 29.85,
                    }
                ]
            }
        }
