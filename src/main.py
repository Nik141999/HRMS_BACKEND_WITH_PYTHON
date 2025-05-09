from fastapi import FastAPI
from src.routes import auth


app = FastAPI(
    title="FastAPI Template",
    version="v0", 
    description="A template for FastAPI projects",
)

app.include_router(auth.router)

@app.get("/", tags=["health"])
async def health():
    return {"massege":"Hello World!"}

