from fastapi import FastAPI
from src.routes import auth,user_route,roles_route,leave_route


app = FastAPI(
    title="FastAPI Template",
    version="v0", 
    description="A template for FastAPI projects",
)

app.include_router(auth.router)
app.include_router(user_route.router)
app.include_router(roles_route.router)
app.include_router(leave_route.router)

@app.get("/", tags=["health"])
async def health():
    return {"massege":"Hello World!"}

