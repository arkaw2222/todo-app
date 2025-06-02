from odmantic import Model
from typing import TypeVar

T = TypeVar("T", bound=Model)

def model_to_clean_dict(model: T) -> T:
    data = model.dict()
    data["id"] = str(model.id)
    return data #type: ignore