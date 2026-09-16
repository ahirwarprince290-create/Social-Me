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
  
