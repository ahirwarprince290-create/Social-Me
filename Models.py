from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base  # database.py se Base connect kiya gaya hai

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # User ke saare posts track karne ke liye relationship
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Post banane wale user ko connect karne ke liye
    author = relationship("User", back_populates="posts")

    __table_args__ = (
        # Feed fast load karne ke liye Composite Index (user_id + created_at)
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

class Like(Base):
    __tablename__ = 'likes'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
  # routers folder ke andar se auth.py ko import karna:
from routers import auth

# Ya auth.py ke andar se specific 'router' object ko import karna:
from routers.auth import router
