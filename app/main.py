from fastapi import FastAPI, Depends

from app.routers.auth import router as auth_router
from app.core.dependencies import get_current_user
from app.models.user import User

from app.routers.jobs import router as jobs_router

from app.routers.applications import router as applications_router

app = FastAPI(
    title="Job Portal API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(jobs_router)
app.include_router(applications_router)


@app.get("/")
def root():
    return {
        "message": "Job Portal API is running"
    }


@app.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }