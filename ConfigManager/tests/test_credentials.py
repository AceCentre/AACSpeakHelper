"""Test module for credential management functionality."""
import os
import sys
import logging
from pathlib import Path

import pytest

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from credential_manager import CredentialManager  # noqa: E402
from encryption import EncryptionManager  # noqa: E402
from tts_manager import MicrosoftClient  # noqa: E402

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture
def credential_manager():
    """Create a credential manager instance for testing."""
    encryption = EncryptionManager()
    return CredentialManager(encryption)


def test_azure_credentials():
    cred_mgr = CredentialManager(EncryptionManager())
    creds = cred_mgr.get_credentials("Azure TTS")
    assert creds is not None
    
    key, region = creds
    client = MicrosoftClient(credentials=(key, region))
    
    voices = client.get_available_voices()
    assert len(voices) > 0


def test_google_credentials(credential_manager):
    """Test Google credentials retrieval."""
    try:
        creds = credential_manager.get_credentials("Google TTS")
        assert creds is not None
        assert len(creds) == 1
        creds_path = creds[0]
        assert os.path.exists(creds_path)
        
        # Verify JSON is valid
        import json
        with open(creds_path) as f:
            creds_json = json.load(f)
        assert "type" in creds_json
        assert "project_id" in creds_json
        logger.info("✓ Google credentials test passed")
    except Exception as e:
        logger.error(f"✗ Google credentials test failed: {e}")
        raise


def test_encryption_key():
    """Test encryption key is available."""
    try:
        key = os.environ.get('CONFIG_ENCRYPTION_KEY')
        assert key is not None and key != ""
        logger.info("✓ Encryption key test passed")
    except Exception as e:
        logger.error(f"✗ Encryption key test failed: {e}")
        raise


if __name__ == "__main__":
    logger.info("Running credential tests...")
    
    # Create managers
    encryption = EncryptionManager()
    cred_mgr = CredentialManager(encryption)
    
    # Run tests
    test_encryption_key()
    test_azure_credentials()
    test_google_credentials(cred_mgr)
    
    logger.info("All tests completed!") 