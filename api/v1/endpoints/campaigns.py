from fastapi import APIRouter, HTTPException
from models.campaign import Campaign, CampaignCreate, CampaignResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[CampaignResponse])
async def read_campaigns():
    campaigns = Campaign.objects.all()
    return [CampaignResponse(**campaign.to_mongo().to_dict()) for campaign in campaigns]

@router.post("/", response_model=CampaignResponse)
async def create_campaign(campaign: CampaignCreate):
    new_campaign = Campaign(**campaign.dict())
    new_campaign.save()
    return CampaignResponse(**new_campaign.to_mongo().to_dict())

@router.get("/{campaign_id}", response_model=CampaignResponse)
async def read_campaign(campaign_id: int):
    campaign = Campaign.objects(campaign_id=campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return CampaignResponse(**campaign.to_mongo().to_dict())

# Add more endpoints as needed
