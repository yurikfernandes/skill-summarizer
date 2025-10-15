from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v, info):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler
    ) -> JsonSchemaValue:
        return {"type": "string", "format": "objectid"}

class Skill(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Python",
                "category": "Programming Language",
                "level": "Avançado"
            }
        }
    )
    
    id: Optional[PyObjectId] = Field(None, alias="_id")
    name: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    level: Optional[str] = Field(None, max_length=20)

class Task(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "title": "Aprender FastAPI",
                "description": "Estudar o framework FastAPI para construção de APIs",
                "extracted_skills": ["Python", "FastAPI", "MongoDB", "RESTful API", "Pydantic"],
                "confirmed_skills": ["Python", "MongoDB", "RESTful API"]
            }
        }
    )
    
    id: Optional[PyObjectId] = Field(None, alias="_id")
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    date: datetime = Field(default_factory=datetime.utcnow)
    extracted_skills: List[str] = Field(default=[])
    confirmed_skills: List[str] = Field(default=[])