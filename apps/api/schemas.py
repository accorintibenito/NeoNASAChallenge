import json
from enum import Enum
from typing import Literal, Annotated, Union
from typing_extensions import Self
from datetime import date, datetime

from pydantic import BaseModel, model_validator, ValidationError, Field
from pydantic.config import ConfigDict

class AsteroidsQueryParams(BaseModel):
    start_date: date
    end_date: date
    hazaourdous: bool | None = None
    sort_by: Literal["distance", "size"] = "distance"
    order: Literal["asc", "desc"] = "asc"
    page: int = 1
    page_size: int = 20

    @model_validator(mode="after")
    def check_end_date_higher_than_start_date(Self) -> Self:
        if Self.end_date<=Self.start_date:
            raise ValueError("A time machine hasn't been invented yet!" \
            "Insert an end-date higher than start-date")
        return Self
    
class AsteroidItem(BaseModel):
    id: int
    name: str
    close_approach_date: date
    miss_distance_km: float
    relative_velocity_kph: float
    estimated_diameter_min_m: float
    estimated_diameter_max_m: float
    is_potentially_hazardous_asteroid: bool
    nasa_jpl_url: str

class Pagination(BaseModel):

class Meta(BaseModel):

class AsteroidsListResponse(BaseModel):
try:
    AsteroidsQueryParams(end_date>=start_date)
except ValidationError as err:
    print(err)
    """
    A time machine was not invented yet, chose an end-date higher than the start-date
    """