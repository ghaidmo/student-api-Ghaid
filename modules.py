from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator


def enum_to_string(cls) -> str:
    return ', '.join([f'{e.name}' for e in cls])


class Gender(Enum):
    male = 'male'
    female = 'female'


class NewStudents(BaseModel):
    name: str = Field(example='name')
    major: str = Field(example='major')
    gender: Gender = Field(example='gender')

    @validator('gender')
    def validate_gender(cls, value: str):
        try:
            value = Gender(value)
        except ValueError:
            ValueError('This gender is not available')
        return value


class NewStudents_Patch(BaseModel):
    name: Optional[str] = Field(example='Name')
    major: Optional[str] = Field(example='major')
    gender: Optional[str] = Field(example='gender')

    @validator('gender')
    def validate_gender(cls, value: str):
        try:
            value = Gender(value)
        except ValueError:
            ValueError('This gender is not available')
        return value
