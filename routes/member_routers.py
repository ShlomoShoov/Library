"""
this file response to the route `/members`

"""
from fastapi import APIRouter, HTTPException
from database.member_db import NewMemberModel, UpdateMemberModel
from database.library_manager import LibraryManager
import database.library_manager as library_manager
manager = LibraryManager()
router = APIRouter(prefix='/members')

@router.post('',status_code=201)
def create_member(data:NewMemberModel):
    try:
        manager.create_member(data=data.model_dump())

    except library_manager.EmailExist:
        raise HTTPException(status_code=400, detail='email is already exists for another user.')
    
@router.get('')
def get_members():
    return manager.get_all_members()

@router.get("/{id}")
def get_member(id:int):
    try:
        return manager.get_member_by_id(member_id=id)
    except library_manager.UserNotExists:
        raise HTTPException(status_code=404, detail=f"{id} -> member not found")
    
    