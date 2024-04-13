import uuid
from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    name: str = Field()
    email: str = Field()
    password: str = Field()
    age: int = Field()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                'id': 'd290f1ee-6c54-4b01-90e6-d701748f0851',
                'name': 'John Doe',
                'email': 'pijus@gmail.com',
                'password': 'password',
                'age': 25
            }
        }

class UserUpdate(BaseModel):
    name: Optional[str] = Field()
    email: Optional[str] = Field()
    age: Optional[int] = Field()

    class Config:
        schema_extra = {
            'example': {
                'name': 'John Doe',
                'email': 'pijus@gmail.com',
                'age': 25,
            }
        }