from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Agentic AI Enterprise Assistant",
    description="A production-grade Enterprise Assistant using RAG with GPT-4",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import and include routers
# from app.routers import auth, query, action, upload
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(query.router, prefix="/query", tags=["Query"])
# app.include_router(action.router, prefix="/action", tags=["Action"])
# app.include_router(upload.router, prefix="/upload", tags=["Upload"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 