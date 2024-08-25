import logging
from fastapi import APIRouter, HTTPException, Query
from models.company import Company, CompanyCreate, CompanyResponse, CompanyUpdate
from typing import List
from mongoengine.errors import ValidationError, DoesNotExist

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[CompanyResponse])
async def read_companies(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    logger.info(f"Fetching companies with skip={skip} and limit={limit}")
    try:
        companies = Company.objects.skip(skip).limit(limit)
        logger.info(f"Successfully fetched {len(companies)} companies")
        return [CompanyResponse.from_mongo(company) for company in companies]
    except Exception as e:
        logger.error(f"Error fetching companies: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while fetching companies")

@router.post("/", response_model=CompanyResponse)
async def create_company(company: CompanyCreate):
    logger.info(f"Creating new company: {company.name}")
    try:
        new_company = Company(**company.model_dump())
        new_company.save()
        logger.info(f"Successfully created company: {new_company.id}")
        return CompanyResponse.from_mongo(new_company)
    except ValidationError as e:
        logger.error(f"Validation error while creating company: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating company: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while creating the company")

@router.get("/{company_id}", response_model=CompanyResponse)
async def read_company(company_id: str):
    logger.info(f"Fetching company with id: {company_id}")
    try:
        company = Company.objects.get(id=company_id)
        logger.info(f"Successfully fetched company: {company_id}")
        return CompanyResponse.from_mongo(company)
    except DoesNotExist:
        logger.warning(f"Company not found: {company_id}")
        raise HTTPException(status_code=404, detail="Company not found")
    except Exception as e:
        logger.error(f"Error fetching company {company_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(company_id: str, company_update: CompanyUpdate):
    logger.info(f"Updating company: {company_id}")
    try:
        company = Company.objects.get(id=company_id)
        for key, value in company_update.model_dump(exclude_unset=True).items():
            setattr(company, key, value)
        company.save()
        logger.info(f"Successfully updated company: {company_id}")
        return CompanyResponse.from_mongo(company)
    except DoesNotExist:
        logger.warning(f"Company not found for update: {company_id}")
        raise HTTPException(status_code=404, detail="Company not found")
    except ValidationError as e:
        logger.error(f"Validation error while updating company {company_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating company {company_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.delete("/{company_id}", response_model=dict)
async def delete_company(company_id: str):
    logger.info(f"Deleting company: {company_id}")
    try:
        company = Company.objects.get(id=company_id)
        company.delete()
        logger.info(f"Successfully deleted company: {company_id}")
        return {"message": "Company deleted successfully"}
    except DoesNotExist:
        logger.warning(f"Company not found for deletion: {company_id}")
        raise HTTPException(status_code=404, detail="Company not found")
    except Exception as e:
        logger.error(f"Error deleting company {company_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
