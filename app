from fastapi import FastAPI
from database import engine, Base
import models

from routers import auth, posts, follows

# Database tables automatically create honge
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Social Media API Backend",
    version="1.0.0"
)

# Root Endpoint (Render "Not Found" fix)
@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Social Media API Backend Active & Working!",
        "docs": "/docs"
    }

# All Routers Connected
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(follows.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
