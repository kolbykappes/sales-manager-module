from fastapi import APIRouter, HTTPException, Query
from models.campaign import Campaign, CampaignCreate, CampaignResponse
from pydantic import TypeAdapter
from typing import List
from mongoengine.errors import ValidationError, DoesNotExist

router = APIRouter()

@router.get("/", response_model=List[CampaignResponse])
async def read_campaigns(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    campaigns = Campaign.objects.skip(skip).limit(limit)
    return TypeAdapter(List[CampaignResponse]).validate_python([campaign.to_mongo().to_dict() for campaign in campaigns])

@router.post("/", response_model=CampaignResponse)
async def create_campaign(campaign: CampaignCreate):
    try:
        new_campaign = Campaign(**campaign.dict())
        new_campaign.save()
        return TypeAdapter(CampaignResponse).validate_python(new_campaign.to_mongo().to_dict())
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{campaign_id}", response_model=CampaignResponse)
async def read_campaign(campaign_id: str):
    try:
        campaign = Campaign.objects.get(campaign_id=campaign_id)
        return TypeAdapter(CampaignResponse).validate_python(campaign.to_mongo().to_dict())
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Campaign not found")

# Add more endpoints as needed
