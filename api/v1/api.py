import logging
from fastapi import APIRouter, Depends, HTTPException
from pymongo.errors import DuplicateKeyError
from .endpoints import campaigns, users, contacts, companies, emails
from config import settings
from models.user import User
from models.campaign import Campaign
from models.company import Company
from models.contact import Contact
from models.email import Email
import json
from mongoengine import connect, disconnect

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

api_router = APIRouter()
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(emails.router, prefix="/emails", tags=["emails"])

@api_router.post("/reset-project", tags=["admin"])
async def reset_project():
    try:
        # Disconnect from the current database
        disconnect()
        # Reconnect to drop the database
        connect(db=settings.DATABASE_NAME, host=settings.MONGODB_URI)
        from mongoengine.connection import get_db
        db = get_db()
        db.client.drop_database(settings.DATABASE_NAME)
        # Reconnect to the fresh database
        connect(db=settings.DATABASE_NAME, host=settings.MONGODB_URI)
        return {
            "message": "Project reset successfully",
            "database_name": settings.DATABASE_NAME,
            "status": "Database dropped and reconnected"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset project: {str(e)}")

@api_router.post("/initialize-db", tags=["admin"])
async def initialize_db():
    logger.info("Starting database initialization")
    try:
        with open(settings.SAMPLE_DATA_FILE, 'r') as file:
            data = json.load(file)
        
        # Create users
        users = {}
        for user_data in data['users']:
            try:
                existing_user = User.objects(email=user_data['email']).first()
                if existing_user:
                    logger.info(f"User with email {user_data['email']} already exists. Updating...")
                    existing_user.is_active = user_data['is_active']
                    existing_user.first_name = user_data['first_name']
                    existing_user.last_name = user_data['last_name']
                    existing_user.set_password(user_data['password'])
                    existing_user.save()
                    users[existing_user.email] = existing_user
                else:
                    user = User(
                        email=user_data['email'],
                        is_active=user_data['is_active'],
                        username=user_data['email'].split('@')[0],  # Using email prefix as username
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name']
                    )
                    user.set_password(user_data['password'])
                    user.save()
                    users[user.email] = user
            except Exception as e:
                logger.error(f"Error creating/updating user {user_data['email']}: {str(e)}")
                continue
        logger.info(f"Created/Updated {len(users)} users")
        
        # Create companies
        companies = {}
        if 'companies' in data:
            for company_data in data['companies']:
                user = users.get(company_data['user_email'])
                if not user:
                    logger.error(f"User with email {company_data['user_email']} not found")
                    continue
                
                existing_company = Company.objects(name=company_data['name']).first()
                if existing_company:
                    logger.info(f"Company {company_data['name']} already exists. Updating...")
                    existing_company.website = company_data.get('website')
                    existing_company.primary_industry = company_data.get('primary_industry')
                    existing_company.primary_sub_industry = company_data.get('primary_sub_industry')
                    existing_company.zoom_id = company_data['zoom_id']
                    existing_company.user = user
                    existing_company.save()
                    companies[existing_company.name] = existing_company
                else:
                    company = Company(
                        name=company_data['name'],
                        website=company_data.get('website'),
                        primary_industry=company_data.get('primary_industry'),
                        primary_sub_industry=company_data.get('primary_sub_industry'),
                        zoom_id=company_data['zoom_id'],
                        user=user
                    )
                    company.save()
                    companies[company.name] = company
            logger.info(f"Created/Updated {len(companies)} companies")
        else:
            logger.error("The 'companies' key is missing in the initialization data.")
            raise HTTPException(status_code=500, detail="Failed to initialize database: 'companies' key missing")
        
        # Create contacts
        contacts_count = 0
        for contact_data in data['contacts']:
            user = users.get(contact_data['user_email'])
            company = companies.get(contact_data['company_name'])
            if not user or not company:
                logger.error(f"User or Company not found for contact: {contact_data['email']}")
                continue
            
            existing_contact = Contact.objects(email=contact_data['email']).first()
            if existing_contact:
                logger.info(f"Contact {contact_data['email']} already exists. Updating...")
                existing_contact.first_name = contact_data['first_name']
                existing_contact.last_name = contact_data['last_name']
                existing_contact.title = contact_data.get('title')
                existing_contact.zoom_id = contact_data['zoom_id']
                existing_contact.user = user
                existing_contact.company = company
                existing_contact.save()
            else:
                contact = Contact(
                    first_name=contact_data['first_name'],
                    last_name=contact_data['last_name'],
                    email=contact_data['email'],
                    title=contact_data.get('title'),
                    zoom_id=contact_data['zoom_id'],
                    user=user,
                    company=company
                )
                contact.save()
            contacts_count += 1
        logger.info(f"Created/Updated {contacts_count} contacts")
        
        # Create campaigns
        campaigns_count = 0
        for campaign_data in data['campaigns']:
            user = users.get(campaign_data['user_email'])
            if not user:
                logger.error(f"User with email {campaign_data['user_email']} not found")
                continue
            
            existing_campaign = Campaign.objects(campaign_name=campaign_data['campaign_name'], user=user).first()
            if existing_campaign:
                logger.info(f"Campaign {campaign_data['campaign_name']} already exists. Updating...")
                existing_campaign.campaign_context = campaign_data['campaign_context']
                existing_campaign.campaign_template_body = campaign_data['campaign_template_body']
                existing_campaign.campaign_template_title = campaign_data['campaign_template_title']
                existing_campaign.save()
            else:
                campaign = Campaign(
                    campaign_name=campaign_data['campaign_name'],
                    campaign_context=campaign_data['campaign_context'],
                    campaign_template_body=campaign_data['campaign_template_body'],
                    campaign_template_title=campaign_data['campaign_template_title'],
                    user=user
                )
                campaign.save()
            campaigns_count += 1
        logger.info(f"Created/Updated {campaigns_count} campaigns")
        
        # Create emails
        emails_count = 0
        for contact in Contact.objects:
            existing_email = Email.objects(contact__email=contact.email).first()
            if existing_email:
                logger.info(f"Email for contact {contact.email} already exists. Skipping...")
                emails_count += 1
                continue
            
            email = Email(
                company={
                    "name": contact.company.name,
                    "zoom_id": contact.company.zoom_id
                },
                contact={
                    "first_name": contact.first_name,
                    "last_name": contact.last_name,
                    "email": contact.email
                },
                subject=f"Sample Email for {contact.first_name}",
                body=f"This is a sample email body for {contact.first_name} {contact.last_name} from {contact.company.name}.",
                ai_model="GPT-3.5",
                tokens_sent=100,
                tokens_returned=150,
                generation_time=0.5,
                campaign_id=Campaign.objects.first().id,
                full_prompt="This is a sample full prompt for email generation."
            )
            email.save()
            emails_count += 1
        logger.info(f"Created {emails_count} emails")
        
        logger.info("Database initialization completed successfully")
        return {"message": "Database initialized with sample data"}
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to initialize database: {str(e)}")

from fastapi import Query
import os

@api_router.get("/logs", tags=["admin"])
async def view_logs(n: int = Query(5, description="Number of log entries to retrieve")):
    try:
        with open('app.log', 'r') as log_file:
            lines = log_file.readlines()
            return {"logs": lines[-n:]}
    except Exception as e:
        logger.error(f"Failed to retrieve logs: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve logs: {str(e)}")

@api_router.post("/reset-logs", tags=["admin"])
async def reset_logs():
    try:
        open('app.log', 'w').close()
        logger.info("Logs have been reset")
        return {"message": "Logs have been reset"}
    except Exception as e:
        logger.error(f"Failed to reset logs: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to reset logs: {str(e)}")

# Add more routers for other endpoints
