#!/usr/bin/env python3
"""
Test suite for configuration loading functionality.
Tests the --config command line argument fix.
"""

import os
import sys
import tempfile
import configparser
import pytest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from configure_enc_utils import load_config


class TestConfigLoading:
    """Test configuration loading with custom paths."""

    def test_load_default_config(self):
        """Test loading default configuration when no custom path is provided."""
        config = load_config()
        assert config is not None
        assert isinstance(config, configparser.ConfigParser)

    def test_load_custom_config_existing_file(self):
        """Test loading a custom configuration file that exists."""
        # Create a temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cfg', delete=False) as f:
            f.write('[App]\n')
            f.write('uuid = test-uuid-123\n')
            f.write('[TTS]\n')
            f.write('engine = azureTTS\n')
            temp_config_path = f.name

        try:
            config = load_config(custom_config_path=temp_config_path)
            assert config is not None
            assert config.get('App', 'uuid') == 'test-uuid-123'
            assert config.get('TTS', 'engine') == 'azureTTS'
        finally:
            os.unlink(temp_config_path)

    def test_load_custom_config_nonexistent_file(self):
        """Test loading a custom configuration file that doesn't exist yet.
        
        This is the key test for the bug fix - the config should be created
        with defaults when the custom path doesn't exist.
        """
        # Use a path that doesn't exist
        temp_dir = tempfile.gettempdir()
        nonexistent_path = os.path.join(temp_dir, 'nonexistent_config_12345.cfg')
        
        # Make sure it doesn't exist
        if os.path.exists(nonexistent_path):
            os.unlink(nonexistent_path)

        try:
            config = load_config(custom_config_path=nonexistent_path)
            assert config is not None
            assert isinstance(config, configparser.ConfigParser)
            # Should have default sections
            assert 'App' in config.sections()
        finally:
            # Clean up
            if os.path.exists(nonexistent_path):
                os.unlink(nonexistent_path)

    def test_custom_path_takes_precedence(self):
        """Test that custom path is used instead of default when provided."""
        # Create two temporary config files with different content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cfg', delete=False) as f:
            f.write('[App]\n')
            f.write('uuid = custom-uuid-456\n')
            custom_config_path = f.name

        try:
            config = load_config(custom_config_path=custom_config_path)
            assert config.get('App', 'uuid') == 'custom-uuid-456'
        finally:
            os.unlink(custom_config_path)

    def test_config_with_multiple_sections(self):
        """Test loading a config with multiple sections."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cfg', delete=False) as f:
            f.write('[App]\n')
            f.write('uuid = test-uuid\n')
            f.write('[TTS]\n')
            f.write('engine = azureTTS\n')
            f.write('[azureTTS]\n')
            f.write('subscription_key = test-key\n')
            f.write('region = eastus\n')
            temp_config_path = f.name

        try:
            config = load_config(custom_config_path=temp_config_path)
            assert 'App' in config.sections()
            assert 'TTS' in config.sections()
            assert 'azureTTS' in config.sections()
            assert config.get('azureTTS', 'subscription_key') == 'test-key'
        finally:
            os.unlink(temp_config_path)

    def test_empty_custom_path_uses_default(self):
        """Test that empty string for custom path uses default."""
        config = load_config(custom_config_path='')
        assert config is not None
        assert isinstance(config, configparser.ConfigParser)

    def test_none_custom_path_uses_default(self):
        """Test that None for custom path uses default."""
        config = load_config(custom_config_path=None)
        assert config is not None
        assert isinstance(config, configparser.ConfigParser)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

