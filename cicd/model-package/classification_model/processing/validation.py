from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from classification_model.config.core import config


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    new_vars_with_na = [
        var
        for var in config.model_config.features
        if var not in config.model_config.numerical_vars_with_na
        and validated_data[var].isnull().sum() > 0
    ]
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    # convert syntax error field names (beginning with numbers)
    # input_data.rename(columns=config.model_config.variables_to_rename, inplace=True)
    input_data["TotalCharges"] = pd.to_numeric(
        input_data["TotalCharges"], errors="coerce"
    )
    relevant_data = input_data[config.model_config.features].copy()
    validated_data = drop_na_inputs(input_data=relevant_data)
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleChurnDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class ChurnDataInputSchema(BaseModel):
    Contract: Optional[str]
    customerID: Optional[str]
    Dependents: Optional[str]
    DeviceProtection: Optional[str]
    gender: Optional[str]
    InternetService: Optional[str]
    MonthlyCharges: Optional[float]
    MultipleLines: Optional[str]
    OnlineBackup: Optional[str]
    OnlineSecurity: Optional[str]
    PaperlessBilling: Optional[str]
    Partner: Optional[str]
    PaymentMethod: Optional[str]
    PhoneService: Optional[str]
    SeniorCitizen: Optional[int]
    StreamingMovies: Optional[str]
    StreamingTV: Optional[str]
    TechSupport: Optional[str]
    tenure: Optional[int]
    TotalCharges: Optional[float]


class MultipleChurnDataInputs(BaseModel):
    inputs: List[ChurnDataInputSchema]
