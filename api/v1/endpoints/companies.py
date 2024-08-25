from fastapi import APIRouter, HTTPException, Query
from models.company import Company, CompanyCreate, CompanyResponse, CompanyUpdate
from typing import List
from mongoengine.errors import ValidationError, DoesNotExist

router = APIRouter()

@router.get("/", response_model=List[CompanyResponse])
async def read_companies(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    companies = Company.objects.skip(skip).limit(limit)
    return [CompanyResponse.from_mongo(company) for company in companies]

@router.post("/", response_model=CompanyResponse)
async def create_company(company: CompanyCreate):
    try:
        new_company = Company(**company.model_dump())
        new_company.save()
        return CompanyResponse.from_mongo(new_company)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{company_id}", response_model=CompanyResponse)
async def read_company(company_id: str):
    try:
        company = Company.objects.get(id=company_id)
        return CompanyResponse.from_mongo(company)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Company not found")

@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(company_id: str, company_update: CompanyUpdate):
    try:
        company = Company.objects.get(id=company_id)
        for key, value in company_update.model_dump(exclude_unset=True).items():
            setattr(company, key, value)
        company.save()
        return CompanyResponse.from_mongo(company)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Company not found")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{company_id}", response_model=dict)
async def delete_company(company_id: str):
    try:
        company = Company.objects.get(id=company_id)
        company.delete()
        return {"message": "Company deleted successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Company not found")
