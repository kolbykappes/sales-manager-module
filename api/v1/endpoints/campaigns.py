from fastapi import APIRouter, HTTPException, Query
from models.campaign import Campaign, CampaignCreate, CampaignResponse
from pydantic import TypeAdapter
from typing import List
from mongoengine.errors import ValidationError, DoesNotExist

router = APIRouter()

@router.get("/", response_model=List[CampaignResponse])
async def read_campaigns(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    campaigns = Campaign.objects.skip(skip).limit(limit)
    return [CampaignResponse.from_mongo(campaign) for campaign in campaigns]

@router.post("/", response_model=CampaignResponse)
async def create_campaign(campaign: CampaignCreate):
    try:
        new_campaign = Campaign(**campaign.model_dump())
        new_campaign.save()
        return CampaignResponse.from_mongo(new_campaign)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{campaign_id}", response_model=CampaignResponse)
async def read_campaign(campaign_id: str):
    try:
        campaign = Campaign.objects.get(campaign_id=campaign_id)
        return CampaignResponse.from_mongo(campaign)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Campaign not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Add more endpoints as needed
