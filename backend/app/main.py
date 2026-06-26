from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.audit import router

app = FastAPI(title="AI UX Auditor", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "AI UX Auditor API is running"}
