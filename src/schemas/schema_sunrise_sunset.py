# -*- coding: utf-8 -*-

from typing import Literal
from pydantic import ValidationError
from pydantic import BaseModel, ConfigDict, model_validator

class Parent(BaseModel):
    model_config = ConfigDict(extra='allow')

class InputSunriseSunsetSchema(Parent):
    model_config = ConfigDict(str_to_lower=True)
    type: str
    latitude: float
    longitude: float

    @model_validator(mode='after')
    def check_type_pattern(self) -> 'InputSunriseSunsetSchema':
        if self.type.lower() not in ('sunrise', 'sunset'):
            raise ValueError(
                'type field can be only [sunrise, sunset]')
        return self

class ExternalSubmmitSunriseSunsetSchema(Parent):
    lat: float
    lng: float
    date: str = None
    callback: str = None
    formatted: int = None
    tzid: str = 'America/Sao_Paulo'

class ExternalResponseSunriseSunsetSchema(Parent):
    results: dict
    status: str
    tzid: str

class OutputSunriseSunsetSchema(Parent):
    remaing_time: str
    exact_datetime: str
    request_datetime: str
