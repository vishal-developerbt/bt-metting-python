from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db
from app.core.security import admin_required

router = APIRouter()

@router.post("/rooms")
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db),current_user: dict = Depends(admin_required)):
    new_room = models.Room(**room.model_dump())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.get("/rooms", response_model=list[schemas.RoomResponse])
def list_rooms(db: Session = Depends(get_db)):
    return db.query(models.Room).all()

@router.put("/rooms/{room_id}")
def update_room(room_id: int, room: schemas.RoomCreate, db: Session = Depends(get_db),current_user: dict = Depends(admin_required)):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")

    db_room.name = room.name
    db_room.capacity = room.capacity
    db_room.location = room.location

    db.commit()
    db.refresh(db_room)
    return db_room

@router.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db),current_user: dict = Depends(admin_required)):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")

    db.delete(db_room)
    db.commit()
    return {"message": "Room deleted"}