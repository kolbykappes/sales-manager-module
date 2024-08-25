import logging
from fastapi import APIRouter, HTTPException, Query
from models.campaign import Campaign, CampaignCreate, CampaignResponse, CampaignUpdate
from pydantic import TypeAdapter
from typing import List
from mongoengine.errors import ValidationError, DoesNotExist

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[CampaignResponse])
async def read_campaigns(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    logger.info(f"Fetching campaigns with skip={skip} and limit={limit}")
    try:
        campaigns = Campaign.objects.skip(skip).limit(limit)
        logger.info(f"Successfully fetched {len(campaigns)} campaigns")
        return [CampaignResponse.from_mongo(campaign) for campaign in campaigns]
    except Exception as e:
        logger.error(f"Error fetching campaigns: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while fetching campaigns")

@router.post("/", response_model=CampaignResponse)
async def create_campaign(campaign: CampaignCreate):
    logger.info(f"Attempting to create new campaign: {campaign.campaign_name}")
    try:
        new_campaign = Campaign(**campaign.model_dump())
        new_campaign.save()
        logger.info(f"Successfully created campaign: {new_campaign.campaign_id}")
        return CampaignResponse.from_mongo(new_campaign)
    except ValidationError as e:
        logger.error(f"Validation error while creating campaign: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error while creating campaign: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/{campaign_id}", response_model=CampaignResponse)
async def read_campaign(campaign_id: str):
    logger.info(f"Fetching campaign with id: {campaign_id}")
    try:
        campaign = Campaign.objects.get(campaign_id=campaign_id)
        logger.info(f"Successfully fetched campaign: {campaign_id}")
        return CampaignResponse.from_mongo(campaign)
    except DoesNotExist:
        logger.warning(f"Campaign not found: {campaign_id}")
        raise HTTPException(status_code=404, detail="Campaign not found")
    except Exception as e:
        logger.error(f"Error fetching campaign {campaign_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(campaign_id: str, campaign_update: CampaignUpdate):
    logger.info(f"Updating campaign: {campaign_id}")
    try:
        campaign = Campaign.objects.get(campaign_id=campaign_id)
        for key, value in campaign_update.model_dump(exclude_unset=True).items():
            setattr(campaign, key, value)
        campaign.save()
        logger.info(f"Successfully updated campaign: {campaign_id}")
        return CampaignResponse.from_mongo(campaign)
    except DoesNotExist:
        logger.warning(f"Campaign not found for update: {campaign_id}")
        raise HTTPException(status_code=404, detail="Campaign not found")
    except ValidationError as e:
        logger.error(f"Validation error while updating campaign {campaign_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating campaign {campaign_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.delete("/{campaign_id}", response_model=dict)
async def delete_campaign(campaign_id: str):
    logger.info(f"Deleting campaign: {campaign_id}")
    try:
        campaign = Campaign.objects.get(campaign_id=campaign_id)
        campaign.delete()
        logger.info(f"Successfully deleted campaign: {campaign_id}")
        return {"message": "Campaign deleted successfully"}
    except DoesNotExist:
        logger.warning(f"Campaign not found for deletion: {campaign_id}")
        raise HTTPException(status_code=404, detail="Campaign not found")
    except Exception as e:
        logger.error(f"Error deleting campaign {campaign_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
