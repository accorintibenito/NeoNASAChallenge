from datetime import date
from typing import Self
from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator



class EstimatedDiameterRange(BaseModel):
    estimated_diameter_min: float = Field(ge=0)
    estimated_diameter_max: float = Field(ge=0)

    @model_validator(mode="after")
    def check_diam_max_ge_min(self) -> Self:
        if self.estimated_diameter_max<=self.estimated_diameter_min:
            raise ValueError("this is not possible, something wrong is happening in NASA systems")
        return self

class EstimatedDiameter(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    kms: EstimatedDiameterRange = Field(alias="kilometers")
    meters: EstimatedDiameterRange
    miles: EstimatedDiameterRange
    feet: EstimatedDiameterRange

class RelativeVelocity(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    kms_per_sec: float = Field(alias="kilometers_per_second", ge=0)
    kms_per_h: float = Field(alias="kilometers_per_hour", ge=0)
    miles_per_h: float = Field(alias="miles_per_hour", ge=0)

    @field_validator("kms_per_sec", "kms_per_h", "miles_per_h", mode="after")
    @classmethod
    def round_value(cls, v: float) -> float:
        return round(v, 2)

class MissDistance(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    astronomical: float = Field(ge=0)
    lunar: float = Field(ge=0)
    kms: float = Field(ge=0, alias="kilometers")
    miles: float = Field(ge=0)

    @field_validator("astronomical", "lunar", "kms", "miles", mode="after")
    @classmethod
    def round_value(cls, v: float) -> float:
        return round(v, 2)

class CloseApproachItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    close_approach_date: date
    rel_velocity: RelativeVelocity = Field(alias="relative_velocity")
    miss_distance: MissDistance = Field(alias="miss_distance")
    orbiting_body: str

class SelfAsteroidLink(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    link: str = Field(alias="self") 

# class AsteroidLink(BaseModel):
#     model_config = ConfigDict(populate_by_name=True)

#     link: SelfAsteroidLink = Field(alias="links")

class Asteroid(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    asteroid_link: SelfAsteroidLink = Field(alias="links")
    id: str
    name: str
    nasa_jpl_url: str
    abs_magn_h: float = Field(ge=0,alias="absolute_magnitude_h")
    estimated_diameter: EstimatedDiameter
    fl_hazardous: bool = Field(alias="is_potentially_hazardous_asteroid")
    close_approach_data: list[CloseApproachItem]

# class SelectedDatesRange(BaseModel):
#     # asteroid: list[Asteroid]
#     date: str = Field(pattern="^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")

# class NearEarthObjects(BaseModel):
#     date: SelectedDatesRange = Field(pattern="^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]")

class NeoWsAPIresponse(BaseModel):
    NEOs: dict[str, list[Asteroid]] = Field(alias="near_earth_objects")

    @field_validator("NEOs", mode="after")
    @classmethod
    def validate_date_keys(cls, v: dict[str, list[Asteroid]]) -> dict[str, list[Asteroid]]:
        for key in v.keys():
            try:
                date.fromisoformat(key)
            except ValueError:
                raise ValueError(f"Invalid date key: {key} coming from the API. Expected real date in YYYY-MM-DD format")
        return v
    # NEOs: NearEarthObjects = Field(alias="near_earth_objects")
    # model_config = ConfigDict(populate_by_name=True)

    # id: str
    # name: str
    # nasa_jpl_url: str
    # abs_magn_h: float = Field(alias="absolute_magnitude_h")
    # estimated_diameter: EstimatedDiameter



    
