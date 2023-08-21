# pylint: disable = unused-argument, no-name-in-module, too-few-public-methods
import random
import json
from typing import List
from pydantic import BaseModel

class OutJsonData(BaseModel):
    """
        output data format
    """
    predictions: List[int]
    prediction_probabilities: List[List[float]]

def send_mock_request(method=None, url=None, headers=None, data=None, timeout=5):
    """
        get a mock / dummy response when
        alignment sheet classification service is called
    """
    output_data = OutJsonData(predictions=[], prediction_probabilities=[])
    
    for _ in json.loads(data)["value"]:
        output_data.predictions.append(random.randint(0, 1))
        output_data.prediction_probabilities.append([0.6, 0.4])

    return output_data
