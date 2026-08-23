from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.user import User
from app.core.dependencies import (
    get_db,
    get_current_user,
    require_employer
)

from app.models.job import Job

from app.schemas.application import ApplicationStatusUpdate

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.get("/")
def get_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "candidate":
        applications = (
            db.query(Application)
            .filter(
                Application.candidate_id == current_user.id
            )
            .all()
        )

    else:
        applications = (
            db.query(Application)
            .join(
                Job,
                Application.job_id == Job.id
            )
            .filter(
                Job.employer_id == current_user.id
            )
            .all()
        )

    return applications

@router.patch("/{application_id}/status")
def update_application_status(
    application_id: int,
    status_data: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_employer)
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    job = (
        db.query(Job)
        .filter(Job.id == application.job_id)
        .first()
    )

    if job.employer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update applications for your own jobs"
        )

    if status_data.status not in ["Accepted", "Rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Accepted or Rejected"
        )

    application.status = status_data.status

    db.commit()
    db.refresh(application)

    return application