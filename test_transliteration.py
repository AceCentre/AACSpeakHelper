#!/usr/bin/env python
"""
test_transliteration.py - Test script for Azure transliteration functionality

This script tests the transliteration implementation to ensure it works correctly
with the provided Azure credentials and follows the same patterns as translation.

Usage:
    python test_transliteration.py

Requirements:
    - Azure Translator credentials in environment variables:
      MICROSOFT_TOKEN_TRANS and MICROSOFT_REGION
    - azure_transliteration.py module
    - Working internet connection

Author: Ace Centre
"""

import os
import sys
import configparser
import logging
from typing import List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_test_config() -> configparser.ConfigParser:
    """Create a test configuration with Azure credentials from environment variables."""
    config = configparser.ConfigParser()
    
    # Get credentials from environment variables
    subscription_key = os.environ.get('MICROSOFT_TOKEN_TRANS', '')
    region = os.environ.get('MICROSOFT_REGION', '')
    
    if not subscription_key or not region:
        raise ValueError(
            "Missing Azure credentials. Please set MICROSOFT_TOKEN_TRANS and MICROSOFT_REGION environment variables."
        )
    
    # Create configuration sections
    config['translate'] = {
        'microsoft_translator_secret_key': subscription_key,
        'region': region
    }
    
    config['transliterate'] = {
        'no_transliterate': 'False',
        'language': 'hi',
        'from_script': 'Latn',
        'to_script': 'Deva',
        'replace_pb': 'True'
    }
    
    return config

def test_basic_transliteration():
    """Test basic transliteration functionality."""
    print("\n=== Testing Basic Transliteration ===")
    
    try:
        from azure_transliteration import AzureTransliterator
        
        # Get credentials from environment
        subscription_key = os.environ.get('MICROSOFT_TOKEN_TRANS', '')
        region = os.environ.get('MICROSOFT_REGION', '')
        
        if not subscription_key or not region:
            print("❌ Missing Azure credentials")
            return False
        
        # Create transliterator
        transliterator = AzureTransliterator(subscription_key, region)
        
        # Test cases: (text, language, from_script, to_script, expected_type)
        test_cases = [
            ("namaste", "hi", "Latn", "Deva", "Hindi Latin to Devanagari"),
            ("hello", "hi", "Latn", "Deva", "English word in Hindi context"),
            ("salam", "ar", "Latn", "Arab", "Arabic Latin to Arabic script"),
        ]
        
        success_count = 0
        for text, lang, from_script, to_script, description in test_cases:
            print(f"\nTesting: {description}")
            print(f"Input: {text} ({lang}: {from_script} → {to_script})")
            
            result = transliterator.transliterate(text, lang, from_script, to_script)
            
            if result is not None:
                print(f"✅ Output: {result}")
                success_count += 1
            else:
                print(f"❌ Failed to transliterate")
        
        print(f"\nBasic transliteration tests: {success_count}/{len(test_cases)} passed")
        return success_count == len(test_cases)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_config_integration():
    """Test transliteration integration with configuration system."""
    print("\n=== Testing Configuration Integration ===")
    
    try:
        from azure_transliteration import transliterate_text
        
        # Create test configuration
        config = create_test_config()
        
        # Test cases with different configurations
        test_cases = [
            ("namaste", "hi", "Latn", "Deva"),
            ("dhanyawad", "hi", "Latn", "Deva"),
            ("salam", "ar", "Latn", "Arab"),
        ]
        
        success_count = 0
        for text, lang, from_script, to_script in test_cases:
            # Update config for this test
            config.set('transliterate', 'language', lang)
            config.set('transliterate', 'from_script', from_script)
            config.set('transliterate', 'to_script', to_script)
            
            print(f"\nTesting config integration: {text} ({lang}: {from_script} → {to_script})")
            
            result = transliterate_text(text, config)
            
            if result is not None:
                print(f"✅ Output: {result}")
                success_count += 1
            else:
                print(f"❌ Failed to transliterate")
        
        print(f"\nConfig integration tests: {success_count}/{len(test_cases)} passed")
        return success_count == len(test_cases)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_server_integration():
    """Test transliteration integration with server processing."""
    print("\n=== Testing Server Integration ===")
    
    try:
        # Import the server function
        sys.path.append('.')
        from AACSpeakHelperServer import transliterate_clipboard
        
        # Create test configuration
        config = create_test_config()
        
        # Test cases
        test_cases = [
            "namaste",
            "dhanyawad", 
            "hello world"
        ]
        
        success_count = 0
        for text in test_cases:
            print(f"\nTesting server integration: {text}")
            
            result = transliterate_clipboard(text, config)
            
            if result is not None:
                print(f"✅ Output: {result}")
                success_count += 1
            else:
                print(f"❌ Failed to transliterate")
        
        print(f"\nServer integration tests: {success_count}/{len(test_cases)} passed")
        return success_count == len(test_cases)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_language_mappings():
    """Test that language and script mappings are properly loaded."""
    print("\n=== Testing Language Mappings ===")
    
    try:
        # Test azure_transliteration module mappings
        from azure_transliteration import TRANSLITERATION_LANGUAGES, TRANSLITERATION_SCRIPTS, COMMON_SCRIPT_PAIRS
        
        print("✅ Azure transliteration mappings loaded successfully")
        print(f"   Languages: {len(TRANSLITERATION_LANGUAGES)} available")
        print(f"   Scripts: {len(TRANSLITERATION_SCRIPTS)} available")
        print(f"   Script pairs: {len(COMMON_SCRIPT_PAIRS)} available")
        
        # Test language_dictionary mappings
        try:
            from GUI_TranslateAndTTS.language_dictionary import (
                Azure_Transliteration_Languages,
                Azure_Transliteration_Scripts,
                Azure_Transliteration_Script_Pairs
            )
            print("✅ Language dictionary mappings loaded successfully")
            print(f"   Languages: {len(Azure_Transliteration_Languages)} available")
            print(f"   Scripts: {len(Azure_Transliteration_Scripts)} available")
            print(f"   Script pairs: {len(Azure_Transliteration_Script_Pairs)} available")
        except ImportError:
            print("⚠️  Language dictionary mappings not found (this is okay)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all transliteration tests."""
    print("🧪 AACSpeakHelper Transliteration Test Suite")
    print("=" * 50)
    
    # Check environment variables
    subscription_key = os.environ.get('MICROSOFT_TOKEN_TRANS', '')
    region = os.environ.get('MICROSOFT_REGION', '')
    
    if not subscription_key or not region:
        print("❌ Missing required environment variables:")
        print("   MICROSOFT_TOKEN_TRANS =", subscription_key[:10] + "..." if subscription_key else "Not set")
        print("   MICROSOFT_REGION =", region or "Not set")
        print("\nPlease set these environment variables and try again.")
        return False
    
    print("✅ Environment variables found:")
    print(f"   MICROSOFT_TOKEN_TRANS = {subscription_key[:10]}...")
    print(f"   MICROSOFT_REGION = {region}")
    
    # Run tests
    tests = [
        ("Language Mappings", test_language_mappings),
        ("Basic Transliteration", test_basic_transliteration),
        ("Configuration Integration", test_config_integration),
        ("Server Integration", test_server_integration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"🧪 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Transliteration implementation is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
