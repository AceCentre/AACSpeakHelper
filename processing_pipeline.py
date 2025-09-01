#!/usr/bin/env python3
"""
Processing Pipeline System for AACSpeakHelper

This module implements a clean, modular processing pipeline that replaces
the confusing boolean logic with an intuitive plugin-based system.
"""

import configparser
import logging
from typing import List, Optional
from abc import ABC, abstractmethod


class ProcessingStep(ABC):
    """Abstract base class for processing steps in the pipeline."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    @abstractmethod
    def is_enabled(self, config: configparser.ConfigParser) -> bool:
        """Check if this processing step is enabled."""
        pass
    
    @abstractmethod
    def process(self, text: str, config: configparser.ConfigParser) -> Optional[str]:
        """Process the text and return the result."""
        pass
    
    def should_replace_clipboard(self, config: configparser.ConfigParser) -> bool:
        """Check if this step should replace the clipboard content (deprecated - use global setting)."""
        # This method is deprecated - clipboard control is now global
        return False


class TranslationStep(ProcessingStep):
    """Translation processing step."""
    
    def __init__(self):
        super().__init__("translate")
    
    def is_enabled(self, config: configparser.ConfigParser) -> bool:
        """Check if translation is enabled (always True if in pipeline)."""
        return True  # If it's in the pipeline, it's enabled
    
    def process(self, text: str, config: configparser.ConfigParser) -> Optional[str]:
        """Perform translation."""
        if not self.is_enabled(config):
            self.logger.debug("Translation disabled, skipping")
            return text
        
        try:
            # Import here to avoid circular imports
            from AACSpeakHelperServer import translate_clipboard
            result = translate_clipboard(text, config)
            
            if result is not None:
                self.logger.info(f"Translation: {text[:50]}... -> {result[:50]}...")
                return result
            else:
                self.logger.warning("Translation failed, using original text")
                return text
                
        except Exception as e:
            self.logger.error(f"Translation error: {e}", exc_info=True)
            return text
    
    def should_replace_clipboard(self, config: configparser.ConfigParser) -> bool:
        """Check if translation should replace clipboard (deprecated - use global setting)."""
        # This method is deprecated - clipboard control is now global
        return False


class TransliterationStep(ProcessingStep):
    """Transliteration processing step."""
    
    def __init__(self):
        super().__init__("transliterate")
    
    def is_enabled(self, config: configparser.ConfigParser) -> bool:
        """Check if transliteration is enabled (always True if in pipeline)."""
        return True  # If it's in the pipeline, it's enabled
    
    def process(self, text: str, config: configparser.ConfigParser) -> Optional[str]:
        """Perform transliteration."""
        if not self.is_enabled(config):
            self.logger.debug("Transliteration disabled, skipping")
            return text
        
        try:
            # Import here to avoid circular imports
            from AACSpeakHelperServer import transliterate_clipboard
            result = transliterate_clipboard(text, config)
            
            if result is not None:
                self.logger.info(f"Transliteration: {text[:50]}... -> {result[:50]}...")
                return result
            else:
                self.logger.warning("Transliteration failed, using original text")
                return text
                
        except Exception as e:
            self.logger.error(f"Transliteration error: {e}", exc_info=True)
            return text
    
    def should_replace_clipboard(self, config: configparser.ConfigParser) -> bool:
        """Check if transliteration should replace clipboard (deprecated - use global setting)."""
        # This method is deprecated - clipboard control is now global
        return False


class TTSStep(ProcessingStep):
    """Text-to-Speech processing step."""
    
    def __init__(self):
        super().__init__("tts")
    
    def is_enabled(self, config: configparser.ConfigParser) -> bool:
        """Check if TTS is enabled (always True if in pipeline)."""
        return True  # If it's in the pipeline, it's enabled
    
    def process(self, text: str, config: configparser.ConfigParser) -> Optional[str]:
        """Perform text-to-speech."""
        if not self.is_enabled(config):
            self.logger.debug("TTS disabled, skipping")
            return text
        
        try:
            # Import here to avoid circular imports
            import tts_utils
            
            # Initialize TTS if needed
            if not tts_utils.ready:
                import utils
                tts_utils.init(utils)
            
            if tts_utils.ready:
                tts_utils.speak(text, False)  # listvoices=False
                self.logger.info(f"TTS: Spoke text of length {len(text)}")
            else:
                self.logger.warning("TTS not ready, skipping speech")
            
            return text  # TTS doesn't modify the text
            
        except Exception as e:
            self.logger.error(f"TTS error: {e}", exc_info=True)
            return text


class ProcessingPipeline:
    """
    Main processing pipeline that orchestrates all processing steps.
    
    This replaces the confusing boolean logic with a clean, modular system.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Register all available processing steps
        self.available_steps = {
            "translate": TranslationStep(),
            "transliterate": TransliterationStep(),
            "tts": TTSStep(),
        }
    
    def get_pipeline_steps(self, config: configparser.ConfigParser) -> List[ProcessingStep]:
        """
        Get the ordered list of processing steps based on configuration.
        
        Uses the new pipeline configuration or falls back to individual enable flags.
        """
        steps = []
        
        # Use pipeline configuration - if it's in the pipeline, it's enabled
        if config.has_option("processing", "pipeline"):
            pipeline_config = config.get("processing", "pipeline", fallback="")
            step_names = [name.strip() for name in pipeline_config.split(",") if name.strip()]

            for step_name in step_names:
                if step_name in self.available_steps:
                    step = self.available_steps[step_name]
                    steps.append(step)
                    self.logger.debug(f"Added {step_name} to pipeline")
                else:
                    self.logger.warning(f"Unknown processing step: {step_name}")
        else:
            # No pipeline config - use empty pipeline
            self.logger.debug("No pipeline config found, no processing steps will be executed")
        
        return steps
    
    def process_text(self, text: str, config: configparser.ConfigParser) -> str:
        """
        Process text through the configured pipeline.
        
        Args:
            text: Input text to process
            config: Configuration object
            
        Returns:
            Processed text
        """
        if not text or not text.strip():
            self.logger.debug("Empty text, skipping processing")
            return text
        
        self.logger.info(f"Starting pipeline processing: {text[:50]}...")
        
        # Get the processing steps
        steps = self.get_pipeline_steps(config)
        
        if not steps:
            self.logger.info("No processing steps enabled, returning original text")
            return text
        
        # Process through each step
        current_text = text

        for step in steps:
            self.logger.debug(f"Processing with {step.name}")

            processed_text = step.process(current_text, config)

            if processed_text is not None:
                current_text = processed_text
            else:
                self.logger.warning(f"{step.name} returned None, continuing with previous text")

        # Handle global clipboard replacement
        should_replace_clipboard = config.getboolean("processing", "replace_clipboard", fallback=False)
        if should_replace_clipboard and current_text != text:
            try:
                import pyperclip
                pyperclip.copy(current_text)
                self.logger.info("Updated clipboard with final processed text")
            except Exception as e:
                self.logger.error(f"Failed to update clipboard: {e}")
        
        self.logger.info(f"Pipeline processing complete: {current_text[:50]}...")
        return current_text


# Global pipeline instance
processing_pipeline = ProcessingPipeline()
