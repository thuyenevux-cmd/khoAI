from typing import Optional
from pydantic import BaseModel, Field

class UnitBase(BaseModel):
    code: str = Field(..., min_length=2, max_length=20)
    name: str = Field(..., min_length=1, max_length=50)

class UnitCreate(UnitBase):
    pass

class UnitResponse(UnitBase):
    id: int

    class Config:
        from_attributes = True
