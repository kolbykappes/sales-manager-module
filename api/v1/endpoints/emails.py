from fastapi import APIRouter, HTTPException, Query
from models.email import Email, EmailCreate, EmailResponse, EmailUpdate
from typing import List
from mongoengine.errors import ValidationError, DoesNotExist

router = APIRouter()

@router.get("/", response_model=List[EmailResponse])
async def read_emails(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    emails = Email.objects.skip(skip).limit(limit)
    return [EmailResponse.from_mongo(email) for email in emails]

@router.post("/", response_model=EmailResponse)
async def create_email(email: EmailCreate):
    try:
        new_email = Email(**email.model_dump())
        new_email.save()
        return EmailResponse.from_mongo(new_email)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{email_id}", response_model=EmailResponse)
async def read_email(email_id: str):
    try:
        email = Email.objects.get(id=email_id)
        return EmailResponse.from_mongo(email)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Email not found")

@router.put("/{email_id}", response_model=EmailResponse)
async def update_email(email_id: str, email_update: EmailUpdate):
    try:
        email = Email.objects.get(id=email_id)
        for key, value in email_update.model_dump(exclude_unset=True).items():
            setattr(email, key, value)
        email.save()
        return EmailResponse.from_mongo(email)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Email not found")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{email_id}", response_model=dict)
async def delete_email(email_id: str):
    try:
        email = Email.objects.get(id=email_id)
        email.delete()
        return {"message": "Email deleted successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Email not found")
