import pytest
from models.campaign import Campaign
from models.user import User

def test_create_campaign(client):
    # Create a test user
    user = User(username="testuser", email="test@example.com", first_name="Test", last_name="User")
    user.set_password("testpassword")
    user.save()

    # Test data
    campaign_data = {
        "campaign_name": "Test Campaign",
        "campaign_context": "Test Context",
        "campaign_template_body": "Test Body",
        "campaign_template_title": "Test Title",
        "user": str(user.id)
    }

    # Make a POST request to create a campaign
    response = client.post("/api/v1/campaigns/", json=campaign_data)

    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["campaign_name"] == campaign_data["campaign_name"]
    assert "campaign_id" in data

    # Clean up
    Campaign.objects.delete()
    User.objects.delete()

def test_get_campaigns(client):
    # Create a test user
    user = User(username="testuser", email="test@example.com", first_name="Test", last_name="User")
    user.set_password("testpassword")
    user.save()

    # Create some test campaigns
    for i in range(3):
        Campaign(
            campaign_name=f"Test Campaign {i}",
            campaign_context="Test Context",
            campaign_template_body="Test Body",
            campaign_template_title="Test Title",
            user=user
        ).save()

    # Make a GET request to fetch campaigns
    response = client.get("/api/v1/campaigns/")

    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    # Clean up
    Campaign.objects.delete()
    User.objects.delete()

def test_get_campaign(client):
    # Create a test user
    user = User(username="testuser", email="test@example.com", first_name="Test", last_name="User")
    user.set_password("testpassword")
    user.save()

    # Create a test campaign
    campaign = Campaign(
        campaign_name="Test Campaign",
        campaign_context="Test Context",
        campaign_template_body="Test Body",
        campaign_template_title="Test Title",
        user=user
    ).save()

    # Make a GET request to fetch the campaign
    response = client.get(f"/api/v1/campaigns/{campaign.campaign_id}")

    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["campaign_name"] == "Test Campaign"
    assert data["campaign_id"] == str(campaign.campaign_id)

    # Clean up
    Campaign.objects.delete()
    User.objects.delete()
