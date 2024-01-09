from fastapi import FastAPI

from src.addresses.router import router as addresses_router
from src.config import app_configs
from src.decisions.router import router as decisions_router
from src.projects.router import router as projects_router
from src.supports.router import router as supports_router
from src.users.router import router as users_router

app = FastAPI(**app_configs)


app.include_router(users_router)
app.include_router(addresses_router)
app.include_router(decisions_router)
app.include_router(supports_router)
app.include_router(projects_router)
