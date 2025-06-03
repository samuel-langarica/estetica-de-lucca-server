import os
import json
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
#load_dotenv()

def get_google_calendar_config():
    """
    Builds the Google Calendar service account configuration from environment variables.
    All environment variables should be prefixed with 'GOOGLE_CALENDAR_'
    """
    try:
        private_key = os.getenv("GOOGLE_CALENDAR_PRIVATE_KEY")
        if not private_key:
            logger.error("GOOGLE_CALENDAR_PRIVATE_KEY environment variable is not set")
            raise ValueError("GOOGLE_CALENDAR_PRIVATE_KEY environment variable is not set")
            
        # Log the first few characters of the private key (safely)
        logger.info(f"Private key starts with: {private_key[:20]}...")
        
        # Ensure proper formatting of the private key
        # First replace literal \n with actual newlines
        private_key = private_key.replace('\\n', '\n')
        # Then ensure we have proper line breaks
        if '\n' not in private_key:
            # If no newlines found, try to add them after every 64 characters
            if len(private_key) > 64:
                parts = []
                for i in range(0, len(private_key), 64):
                    parts.append(private_key[i:i+64])
                private_key = '\n'.join(parts)
        
        # Validate private key format
        if not private_key.startswith('-----BEGIN PRIVATE KEY-----'):
            logger.error("Private key is missing BEGIN marker")
            raise ValueError("Private key must start with '-----BEGIN PRIVATE KEY-----'")
            
        if not private_key.endswith('-----END PRIVATE KEY-----'):
            logger.error("Private key is missing END marker")
            raise ValueError("Private key must end with '-----END PRIVATE KEY-----'")
            
        # Check if the key has proper line breaks
        if '\n' not in private_key:
            logger.error("Private key is missing line breaks")
            raise ValueError("Private key must contain line breaks")
            
        # Check if the key has the proper structure
        key_parts = private_key.split('\n')
        if len(key_parts) < 3:
            logger.error("Private key has invalid structure")
            raise ValueError("Private key must have at least 3 lines (BEGIN, content, END)")
            
        config = {
            "type": os.getenv("GOOGLE_CALENDAR_TYPE", "service_account"),
            "project_id": os.getenv("GOOGLE_CALENDAR_PROJECT_ID"),
            "private_key_id": os.getenv("GOOGLE_CALENDAR_PRIVATE_KEY_ID"),
            "private_key": private_key,
            "client_email": os.getenv("GOOGLE_CALENDAR_CLIENT_EMAIL"),
            "client_id": os.getenv("GOOGLE_CALENDAR_CLIENT_ID"),
            "auth_uri": os.getenv("GOOGLE_CALENDAR_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
            "token_uri": os.getenv("GOOGLE_CALENDAR_TOKEN_URI", "https://oauth2.googleapis.com/token"),
            "auth_provider_x509_cert_url": os.getenv("GOOGLE_CALENDAR_AUTH_PROVIDER_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
            "client_x509_cert_url": os.getenv("GOOGLE_CALENDAR_CLIENT_CERT_URL"),
            "universe_domain": os.getenv("GOOGLE_CALENDAR_UNIVERSE_DOMAIN", "googleapis.com")
        }
        
        # Log configuration details (safely)
        logger.info(f"Configuration loaded with project_id: {config['project_id']}")
        logger.info(f"Client email: {config['client_email']}")
        
        # Validate required fields
        required_fields = ['project_id', 'private_key_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if not config.get(field)]
        
        if missing_fields:
            logger.error(f"Missing required environment variables: {', '.join(missing_fields)}")
            raise ValueError(f"Missing required environment variables: {', '.join(missing_fields)}")
        
        logger.info("Successfully loaded Google Calendar configuration")
        return config
        
    except Exception as e:
        logger.error(f"Error loading Google Calendar configuration: {str(e)}")
        raise

def get_google_calendar_json():
    """
    Returns the Google Calendar configuration as a JSON string
    """
    try:
        config = get_google_calendar_config()
        return json.dumps(config, indent=2)
    except Exception as e:
        logger.error(f"Error converting configuration to JSON: {str(e)}")
        raise 