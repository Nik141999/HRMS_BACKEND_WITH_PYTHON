from fastapi import FastAPI
from src.routes import auth,user_route,roles_route,leave_route
from fastapi.middleware.cors import CORSMiddleware  # ✅ Import CORS



app = FastAPI(
    title="FastAPI Template",
    version="v0", 
    description="A template for FastAPI projects",
)

# ✅ Add CORS Middleware
origins = [
    "http://localhost:3000",   # React frontend
    "http://127.0.0.1:3000"
    # You can also add other domains if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Domains allowed
    allow_credentials=True,
    allow_methods=["*"],             # Allow all HTTP methods
    allow_headers=["*"],             # Allow all headers
)


app.include_router(auth.router)
app.include_router(user_route.router)
app.include_router(roles_route.router)
app.include_router(leave_route.router)

@app.get("/", tags=["health"])
async def health():
    return {"massege":"Hello World!"}

