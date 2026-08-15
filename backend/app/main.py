from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analysis import router as analysis_router
from app.routes.search import router as search_router
from app.routes.services import router as services_router


app = FastAPI(
    title="AI DevOps Incident Graph",
    description="Graph-powered DevOps incident investigation API",
    version="1.0.0",
)


# Allow the React frontend to communicate with the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(services_router)
app.include_router(analysis_router)
app.include_router(search_router)


@app.get("/")
def root():
    return {
        "name": "AI DevOps Incident Graph",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }