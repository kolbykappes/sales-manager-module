from fastapi import APIRouter, HTTPException, Query
from models.contact import Contact, ContactCreate, ContactResponse, ContactUpdate
from typing import List
from mongoengine.errors import ValidationError, DoesNotExist

router = APIRouter()

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    contacts = Contact.objects.skip(skip).limit(limit)
    return [ContactResponse.from_mongo(contact) for contact in contacts]

@router.post("/", response_model=ContactResponse)
async def create_contact(contact: ContactCreate):
    try:
        new_contact = Contact(**contact.model_dump())
        new_contact.save()
        return ContactResponse.from_mongo(new_contact)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: str):
    try:
        contact = Contact.objects.get(id=contact_id)
        return ContactResponse.from_mongo(contact)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Contact not found")

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: str, contact_update: ContactUpdate):
    try:
        contact = Contact.objects.get(id=contact_id)
        for key, value in contact_update.model_dump(exclude_unset=True).items():
            setattr(contact, key, value)
        contact.save()
        return ContactResponse.from_mongo(contact)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Contact not found")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{contact_id}", response_model=dict)
async def delete_contact(contact_id: str):
    try:
        contact = Contact.objects.get(id=contact_id)
        contact.delete()
        return {"message": "Contact deleted successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Contact not found")
