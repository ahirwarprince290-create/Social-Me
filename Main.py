from fastapi import FastAPI
from database import engine, Base
from routers import auth, posts, follows

# Sabhi DB Tables aur Indexes create karne ke liye
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Modular Social Media Backend API")

# Separate routers include karna
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(follows.router)

@app.get("/")
def home():
    return {"status": "ok", "message": "Social Media Modular Backend Running"}
 from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from datetime import datetime
from database import Base  # <--- database.py se Base import kiya

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_user_posts', 'user_id', 'created_at'),
    )

class Follow(Base):
    __tablename__ = 'follows'

    follower_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    following_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_follower', 'follower_id'),
        Index('idx_following', 'following_id'),
    )
    
