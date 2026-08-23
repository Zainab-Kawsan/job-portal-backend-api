from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate,JobUpdate, JobResponse
from app.core.dependencies import get_db, require_employer,require_candidate

from app.models.application import Application

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post(
    "/",
    response_model=JobResponse
)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_employer)
):
    new_job = Job(
        title=job_data.title,
        company=job_data.company,
        location=job_data.location,
        salary=job_data.salary,
        description=job_data.description,
        employer_id=current_user.id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

@router.get("/", response_model=list[JobResponse])
def get_jobs(
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).all()

    return jobs

@router.get(
    "/{job_id}",
    response_model=JobResponse
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job

@router.put(
    "/{job_id}",
    response_model=JobResponse
)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_employer)
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if job.employer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own jobs"
        )

    job.title = job_data.title
    job.company = job_data.company
    job.location = job_data.location
    job.salary = job_data.salary
    job.description = job_data.description

    db.commit()
    db.refresh(job)

    return job

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_employer)
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if job.employer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own jobs"
        )

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully"
    }
    
    
@router.post("/{job_id}/apply")
def apply_for_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_candidate)
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    existing_application = (
        db.query(Application)
        .filter(
            Application.job_id == job_id,
            Application.candidate_id == current_user.id
        )
        .first()
    )

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="You already applied for this job"
        )

    application = Application(
        job_id=job_id,
        candidate_id=current_user.id
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application