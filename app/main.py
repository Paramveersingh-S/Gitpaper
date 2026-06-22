from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import webhook, oauth, dashboard, health
from app.database import engine, Base
from app.config import settings

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GitPaper",
    description="Link your code to the research papers it implements",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, tags=["health"])
app.include_router(webhook.router, tags=["webhooks"])
app.include_router(oauth.router, prefix="/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])


@app.get("/")
async def root():
    return {
        "name": "GitPaper",
        "status": "running",
        "install_url": f"https://github.com/apps/gitpaper/installations/new",
    }
