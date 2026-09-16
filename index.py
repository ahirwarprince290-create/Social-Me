from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, Post

DATABASE_URL = "sqlite:///./social_app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database Tables aur Indexes automatically create honge
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Social Media API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index_root():
    return {"status": "online", "message": "Social Media API Ready"}

@app.get("/feed/{user_id}")
def get_user_feed(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    # Composite Index (idx_user_posts) is query ko optimized execution deta hai
    posts = (
        db.query(Post)
        .filter(Post.user_id == user_id)
        .order_by(Post.created_at.desc())
        .limit(limit)
        .all()
    )
    return {"user_id": user_id, "posts": posts}
  
