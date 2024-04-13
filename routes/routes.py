from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder

from typing import List

from models.models import User, UserUpdate

router = APIRouter()

@router.post('/', response_description='Adds new user', status_code=status.HTTP_201_CREATED ,response_model=User)
def create_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)

    existing = request.app.database['users'].find_one({ 'email': user['email'] })

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = request.app.database['users'].insert_one(user)
    created_user = request.app.database['users'].find_one({'_id': new_user.inserted_id})
    return created_user

@router.get('/', response_description='Returns all users', response_model=List[User])
def get_users(request: Request):
    users = request.app.database['users'].find()
    return users

@router.get('/{id}', response_description='Returns a single user', response_model=User)
def get_user(request: Request, id: str):
    user = request.app.database['users'].find_one({'_id': id})
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.put('/{id}', response_description='Updates a user', response_model=User)
def update_user(request: Request, id: str, user: UserUpdate = Body(...)):
    user = {k: v for k, v in user.model_dump().items() if v is not None}
    if len(user) >= 1:
        updated_user = request.app.database['users'].update_one({'_id': id}, {'$set': user})
        if updated_user.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        if (
            existing := request.app.database['users'].find_one({'_id': id})
        ) is not None:
            return existing

    raise HTTPException(status_code=400, detail="No fields to update provided")

@router.delete('/{id}', response_description='Deletes a user')
def delete_user(request: Request, id: str):
    deleted_user = request.app.database['users'].delete_one({'_id': id})
    if deleted_user.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="User not found")