#!/usr/bin/env python3
"""Test script for Microsoft Translator functionality"""

import configparser
import os
import processing_pipeline

def test_translation():
    print('=== Testing Microsoft Translator API ===')
    
    # Set environment variable
    os.environ['MICROSOFT_TOKEN_TRANS'] = '0844548f3ef64ba9858dd31cd44dc24a'
    
    # Load config
    config = configparser.ConfigParser()
    config.read('config_translation_only.cfg')
    
    # Test translation using processing pipeline
    try:
        pipeline = processing_pipeline.ProcessingPipeline()
        result = pipeline.process_text('Hello world', config)
        print('Original text: Hello world')
        print('Processed text:', result)

        # Check if translation was applied (should be different from original)
        if result != 'Hello world':
            print('Translation successful!')
            return True
        else:
            print('No translation applied (text unchanged)')
            return False
    except Exception as e:
        print('Processing error:', str(e))
        return False

if __name__ == '__main__':
    test_translation()
