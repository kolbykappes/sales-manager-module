import logging
from fastapi import APIRouter, HTTPException, Query
from models.email import Email, EmailCreate, EmailResponse, EmailUpdate
from typing import List
from mongoengine.errors import ValidationError, DoesNotExist

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[EmailResponse])
async def read_emails(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    logger.info(f"Fetching emails with skip={skip} and limit={limit}")
    try:
        emails = Email.objects.skip(skip).limit(limit)
        logger.info(f"Successfully fetched {len(emails)} emails")
        return [EmailResponse.from_mongo(email) for email in emails]
    except Exception as e:
        logger.error(f"Error fetching emails: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while fetching emails")

@router.post("/", response_model=EmailResponse)
async def create_email(email: EmailCreate):
    logger.info(f"Creating new email: {email.subject}")
    try:
        new_email = Email(**email.model_dump())
        new_email.save()
        logger.info(f"Successfully created email: {new_email.id}")
        return EmailResponse.from_mongo(new_email)
    except ValidationError as e:
        logger.error(f"Validation error while creating email: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating email: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while creating the email")

@router.get("/{email_id}", response_model=EmailResponse)
async def read_email(email_id: str):
    logger.info(f"Fetching email with id: {email_id}")
    try:
        email = Email.objects.get(id=email_id)
        logger.info(f"Successfully fetched email: {email_id}")
        return EmailResponse.from_mongo(email)
    except DoesNotExist:
        logger.warning(f"Email not found: {email_id}")
        raise HTTPException(status_code=404, detail="Email not found")
    except Exception as e:
        logger.error(f"Error fetching email {email_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/{email_id}", response_model=EmailResponse)
async def update_email(email_id: str, email_update: EmailUpdate):
    logger.info(f"Updating email: {email_id}")
    try:
        email = Email.objects.get(id=email_id)
        for key, value in email_update.model_dump(exclude_unset=True).items():
            setattr(email, key, value)
        email.save()
        logger.info(f"Successfully updated email: {email_id}")
        return EmailResponse.from_mongo(email)
    except DoesNotExist:
        logger.warning(f"Email not found for update: {email_id}")
        raise HTTPException(status_code=404, detail="Email not found")
    except ValidationError as e:
        logger.error(f"Validation error while updating email {email_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating email {email_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.delete("/{email_id}", response_model=dict)
async def delete_email(email_id: str):
    logger.info(f"Deleting email: {email_id}")
    try:
        email = Email.objects.get(id=email_id)
        email.delete()
        logger.info(f"Successfully deleted email: {email_id}")
        return {"message": "Email deleted successfully"}
    except DoesNotExist:
        logger.warning(f"Email not found for deletion: {email_id}")
        raise HTTPException(status_code=404, detail="Email not found")
    except Exception as e:
        logger.error(f"Error deleting email {email_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
