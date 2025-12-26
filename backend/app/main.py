from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .routers import resume, jobs, recommendations, llm, analytics
from .models import Base
from .database import engine

app = FastAPI(title="AI Resume CoPilot API")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"ok": True}

app.include_router(resume.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(llm.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    print("UNHANDLED:", repr(exc))
    return JSONResponse(status_code=500, content={"detail": str(exc)})
