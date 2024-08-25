import logging
from fastapi import APIRouter, HTTPException, Query
from models.contact import Contact, ContactCreate, ContactResponse, ContactUpdate
from typing import List
from mongoengine.errors import ValidationError, DoesNotExist

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    logger.info(f"Fetching contacts with skip={skip} and limit={limit}")
    try:
        contacts = Contact.objects.skip(skip).limit(limit)
        logger.info(f"Successfully fetched {len(contacts)} contacts")
        return [ContactResponse.from_mongo(contact) for contact in contacts]
    except Exception as e:
        logger.error(f"Error fetching contacts: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while fetching contacts")

@router.post("/", response_model=ContactResponse)
async def create_contact(contact: ContactCreate):
    logger.info(f"Creating new contact: {contact.email}")
    try:
        new_contact = Contact(**contact.model_dump())
        new_contact.save()
        logger.info(f"Successfully created contact: {new_contact.id}")
        return ContactResponse.from_mongo(new_contact)
    except ValidationError as e:
        logger.error(f"Validation error while creating contact: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating contact: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while creating the contact")

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: str):
    logger.info(f"Fetching contact with id: {contact_id}")
    try:
        contact = Contact.objects.get(id=contact_id)
        logger.info(f"Successfully fetched contact: {contact_id}")
        return ContactResponse.from_mongo(contact)
    except DoesNotExist:
        logger.warning(f"Contact not found: {contact_id}")
        raise HTTPException(status_code=404, detail="Contact not found")
    except Exception as e:
        logger.error(f"Error fetching contact {contact_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: str, contact_update: ContactUpdate):
    logger.info(f"Updating contact: {contact_id}")
    try:
        contact = Contact.objects.get(id=contact_id)
        for key, value in contact_update.model_dump(exclude_unset=True).items():
            setattr(contact, key, value)
        contact.save()
        logger.info(f"Successfully updated contact: {contact_id}")
        return ContactResponse.from_mongo(contact)
    except DoesNotExist:
        logger.warning(f"Contact not found for update: {contact_id}")
        raise HTTPException(status_code=404, detail="Contact not found")
    except ValidationError as e:
        logger.error(f"Validation error while updating contact {contact_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating contact {contact_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.delete("/{contact_id}", response_model=dict)
async def delete_contact(contact_id: str):
    logger.info(f"Deleting contact: {contact_id}")
    try:
        contact = Contact.objects.get(id=contact_id)
        contact.delete()
        logger.info(f"Successfully deleted contact: {contact_id}")
        return {"message": "Contact deleted successfully"}
    except DoesNotExist:
        logger.warning(f"Contact not found for deletion: {contact_id}")
        raise HTTPException(status_code=404, detail="Contact not found")
    except Exception as e:
        logger.error(f"Error deleting contact {contact_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
