#!/usr/bin/env python3
"""
Configuration Migration System for AACSpeakHelper

This module provides backward compatibility while transitioning to a cleaner,
more intuitive configuration system.
"""

import configparser
import logging
from typing import Dict, Any, Optional


class ConfigMigrator:
    """
    Handles migration from old negative boolean configuration to new positive configuration.
    Provides backward compatibility while encouraging migration to the new system.
    """

    # Mapping from old negative keys to new positive keys
    MIGRATION_MAP = {
        ("translate", "no_translate"): ("translate", "enabled", "invert"),
        ("transliterate", "no_transliterate"): ("transliterate", "enabled", "invert"),
        ("tts", "bypass_tts"): ("tts", "enabled", "invert"),
        ("translate", "source_language"): ("translate", "source_language", "direct"),
        ("translate", "target_language"): ("translate", "target_language", "direct"),
        ("translate", "replace_pb"): ("translate", "replace_clipboard", "direct"),
        ("tts", "save_audio_file"): ("tts", "save_audio", "direct"),
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def migrate_config(
        self, config: configparser.ConfigParser
    ) -> configparser.ConfigParser:
        """
        Migrate old configuration format to new format.

        Args:
            config: ConfigParser with old format

        Returns:
            ConfigParser with new format (backward compatible)
        """
        migrated_config = configparser.ConfigParser()

        # Copy all existing sections first
        for section_name in config.sections():
            migrated_config.add_section(section_name)
            for key, value in config[section_name].items():
                migrated_config.set(section_name, key, value)

        # Add new sections if they don't exist
        for new_section in ["processing", "translate", "transliterate", "tts"]:
            if not migrated_config.has_section(new_section):
                migrated_config.add_section(new_section)

        # Migrate values using mapping
        for (old_section, old_key), (
            new_section,
            new_key,
            transform,
        ) in self.MIGRATION_MAP.items():
            if config.has_option(old_section, old_key):
                old_value = config.get(old_section, old_key)

                if transform == "invert":
                    # Convert negative boolean to positive
                    new_value = "false" if old_value.lower() == "true" else "true"
                elif transform == "direct":
                    # Direct copy
                    new_value = old_value
                else:
                    new_value = old_value

                migrated_config.set(new_section, new_key, new_value)
                self.logger.info(
                    f"Migrated {old_section}.{old_key}={old_value} -> {new_section}.{new_key}={new_value}"
                )

        # Set up default processing pipeline
        if not migrated_config.has_option("processing", "pipeline"):
            # Determine pipeline based on enabled features
            pipeline_steps = []

            if migrated_config.getboolean("translate", "enabled", fallback=False):
                pipeline_steps.append("translate")

            if migrated_config.getboolean("transliterate", "enabled", fallback=False):
                pipeline_steps.append("transliterate")

            if migrated_config.getboolean("tts", "enabled", fallback=True):
                pipeline_steps.append("tts")

            migrated_config.set("processing", "pipeline", ",".join(pipeline_steps))

        return migrated_config

    def get_boolean_with_fallback(
        self,
        config: configparser.ConfigParser,
        section: str,
        key: str,
        fallback: bool = False,
    ) -> bool:
        """
        Get boolean value - new positive format only.
        """
        return config.getboolean(section, key, fallback=fallback)

    def get_string_with_fallback(
        self,
        config: configparser.ConfigParser,
        section: str,
        key: str,
        fallback: str = "",
    ) -> str:
        """
        Get string value - new format only.
        """
        return config.get(section, key, fallback=fallback)


# Global instance for easy access
config_migrator = ConfigMigrator()
