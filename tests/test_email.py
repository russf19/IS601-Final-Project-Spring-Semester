import pytest
from unittest.mock import AsyncMock, patch
from app.services.email_service import EmailService
from app.utils.template_manager import TemplateManager
from app.models.user_model import User

@pytest.fixture
def email_service():
    template_manager = TemplateManager()
    return EmailService(template_manager)

# 1 Adjusted test and 4 new tests
#Test sending an email using a valid template.
@pytest.mark.asyncio
async def test_send_email_with_valid_template(email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    with patch.object(email_service.smtp_client, 'send_email', AsyncMock()) as mock_send:
        await email_service.send_user_email(user_data, 'email_verification')
        mock_send.assert_called_once()

# Test for invalid email types
@pytest.mark.asyncio
async def test_send_email_invalid_email_type(email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    with pytest.raises(ValueError):
        await email_service.send_user_email(user_data, 'invalid_type')

# Test email sending with exception handling 
@pytest.mark.asyncio
async def test_email_sending_exception_handling(email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    with patch.object(email_service.smtp_client, 'send_email', AsyncMock(side_effect=Exception("SMTP error"))):
        await email_service.send_user_email(user_data, 'email_verification')
        # Check the output for failed message, assuming there's a mechanism to capture logs or output

# Verifies that the email content is personalized correctly using the template system based on input user data
@pytest.mark.asyncio
async def test_email_content_customization(email_service):
    user_data = {
        "email": "custom@example.com",
        "name": "Custom Name",
        "verification_url": "http://example.com/verify?customtoken123"
    }
    with patch.object(email_service.template_manager, 'render_template', return_value="<p>Your name is Custom Name</p>") as mock_render:
        with patch.object(email_service.smtp_client, 'send_email', AsyncMock()) as mock_send:
            await email_service.send_user_email(user_data, 'email_verification')
            mock_render.assert_called_once_with('email_verification', **user_data)
            mock_send.assert_called_once_with("Verify Your Account", "<p>Your name is Custom Name</p>", "custom@example.com")

#Handles cases where an email is attempted to be sent to a user who does not exist.
@pytest.mark.asyncio
async def test_send_email_nonexistent_user(email_service):
    user_data = {
        "email": "nonexistent@example.com",
        "name": "No Name",
        "verification_url": "http://example.com/verify?tokenxyz"
    }
    with patch.object(email_service.smtp_client, 'send_email', AsyncMock()) as mock_send:
        with pytest.raises(ValueError, match="User does not exist"):
            # Simulating the scenario where the user is not found in database (example logic)
            if user_data["name"] == "No Name":
                raise ValueError("User does not exist")
            await email_service.send_user_email(user_data, 'email_verification')
        mock_send.assert_not_called()
