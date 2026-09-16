from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Post
from pydantic import BaseModel

router = APIRouter(prefix="/posts", tags=["Posts & Timeline Feed"])

class PostCreate(BaseModel):
    user_id: int
    content: str

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_post(post_data: PostCreate, db: Session = Depends(get_db)):
    post = Post(user_id=post_data.user_id, content=post_data.content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"message": "Post published", "post_id": post.id}

@router.get("/feed/{user_id}")
def fetch_timeline_feed(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    # Composite Index (user_id + created_at) is query ki performance speed badhata hai
    posts = (
        db.query(Post)
        .filter(Post.user_id == user_id)
        .order_by(Post.created_at.desc())
        .limit(limit)
        .all()
    )
    return {"user_id": user_id, "feed_count": len(posts), "posts": posts}
  from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db  # <--- database.py se import
from models import Post       # <--- models.py se import
from pydantic import BaseModel

router = APIRouter(prefix="/posts", tags=["Posts Feed"])

class PostCreate(BaseModel):
    user_id: int
    content: str

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    post = Post(user_id=post_data.user_id, content=post_data.content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"message": "Post created", "post_id": post.id}

@router.get("/feed/{user_id}")
def get_feed(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    posts = (
        db.query(Post)
        .filter(Post.user_id == user_id)
        .order_by(Post.created_at.desc())
        .limit(limit)
        .all()
    )
    return {"user_id": user_id, "posts": posts}
    
