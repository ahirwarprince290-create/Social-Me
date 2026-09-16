from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Follow

router = APIRouter(prefix="/social", tags=["Social Network & Follows"])

@router.post("/follow")
def follow_user(follower_id: int, following_id: int, db: Session = Depends(get_db)):
    if follower_id == following_id:
        raise HTTPException(status_code=400, detail="Self-following not allowed")
    
    follow_record = Follow(follower_id=follower_id, following_id=following_id)
    db.add(follow_record)
    db.commit()
    return {"message": f"User {follower_id} started following User {following_id}"}
  
