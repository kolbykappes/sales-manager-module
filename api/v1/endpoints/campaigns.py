from fastapi import APIRouter, HTTPException, Depends
from models.campaign import Campaign
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Campaign])
async def read_campaigns():
    return list(Campaign.objects.all())

@router.post("/", response_model=Campaign)
async def create_campaign(campaign: Campaign):
    return campaign.save()

@router.get("/{campaign_id}", response_model=Campaign)
async def read_campaign(campaign_id: int):
    campaign = Campaign.objects(campaign_id=campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

# Add more endpoints as needed
