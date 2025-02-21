# File: config_manager.py
import logging
import dearpygui.dearpygui as dpg
from encryption import EncryptionManager
from credential_manager import CredentialManager
from tts_manager import TTSManager
from ui_components import (
    create_voice_table,
    create_translation_tab, 
    create_settings_tab,
    get_setting,
    get_translate_setting,
    show_success_dialog,
    show_error_dialog,
    show_info_dialog
)
import os
from translation_manager import TranslationManager

class ConfigManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.encryption = EncryptionManager()
        self.cred_mgr = CredentialManager(self.encryption)
        self.tts_mgr = TTSManager()
        self.translation_mgr = TranslationManager()
        self.window_tag = "main_window"  # Add tag for the window

    def create_main_window(self):
        # Create viewport first
        dpg.create_viewport(
            title="AACSpeakHelper Config",
            width=1000,
            height=800,
            min_width=800,
            min_height=600
        )

        # Load font with international character support
        with dpg.font_registry():
            default_font = dpg.add_font(
                "assets/NotoSans-Regular.ttf", 
                16
            )
            dpg.bind_font(default_font)

        # Load and set icon - using PNG instead of ICO
        icon_path = os.path.join(os.path.dirname(__file__), "assets/configure.png")
        if os.path.exists(icon_path):
            try:
                width, height, channels, data = dpg.load_image(icon_path)
                with dpg.texture_registry():
                    texture_id = dpg.add_static_texture(width, height, data)
                    dpg.configure_viewport(0, small_icon=texture_id)
            except Exception as e:
                self.logger.warning(f"Could not load icon: {e}")

        with dpg.window(
            label="AACSpeakHelper Configuration",
            tag=self.window_tag,
            pos=(100, 100),
            no_resize=False
        ):
            # Add styling
            with dpg.theme() as global_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (37, 37, 38))
                    dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30))
                    dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))
                    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                    dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)

            dpg.bind_theme(global_theme)

            # Create horizontal group for tabs and buttons
            with dpg.group(horizontal=True):
                # Tab bar with width to leave space for buttons
                with dpg.child_window(width=-200, border=False):
                    with dpg.tab_bar():
                        self._create_tts_tab()
                        self._create_translation_tab()
                        self._create_settings_tab()
                
                # Buttons on the right
                with dpg.group():
                    dpg.add_button(
                        label="Save Changes",  # More descriptive label
                        callback=self._save_all_settings,
                        width=150,
                        height=35
                    )
                    dpg.add_spacer(height=5)
                    dpg.add_button(
                        label="Revert Changes",  # More descriptive than "Discard"
                        callback=self._discard_changes,
                        width=150,
                        height=35
                    )

                    # Add some styling to make Save more prominent
                    with dpg.theme() as save_theme:
                        with dpg.theme_component(dpg.mvButton):
                            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 120, 255))
                            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (65, 155, 255))
                            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 95, 200))
                    dpg.bind_item_theme(dpg.last_item(), save_theme)

    def _create_tts_tab(self):
        with dpg.tab(label="TTS Engines"):
            with dpg.group(horizontal=True):
                # Left side - engine selection and voice table
                with dpg.child_window(width=-250):  # Leave 250px for right panel
                    with dpg.group():
                        engine_names = self.tts_mgr.get_engine_names()
                        dpg.add_combo(
                            items=engine_names,
                            label="Select Engine",
                            callback=self._on_engine_selected,
                            default_value=engine_names[0] if engine_names else ""
                        )
                        
                        dpg.add_spacer(height=10)
                        
                        # Create a permanent container for credentials
                        dpg.add_group(tag="credentials_container")
                        self._create_credential_inputs(engine_names[0] if engine_names else None)
                        
                        # Add voice table container here
                        dpg.add_child_window(tag="voice_table_container", border=True)
                        if engine_names:
                            create_voice_table(self.tts_mgr, engine_names[0])

                # Right side - current settings
                with dpg.child_window(width=250, border=True):
                    dpg.add_text("Current Settings", color=(255, 255, 0))
                    dpg.add_separator()
                    
                    # Active TTS Engine
                    dpg.add_text("TTS Engine:")
                    dpg.add_text(
                        get_setting('tts', 'engine', 'None'),
                        color=(0, 255, 0),
                        tag="active_engine_display"
                    )
                    
                    # Active Voice
                    dpg.add_text("Voice:")
                    dpg.add_text(
                        get_setting('tts', 'voice_name', 'None'),
                        color=(0, 255, 0),
                        tag="active_voice_display"
                    )
                    
                    # Translation Settings
                    dpg.add_separator()
                    dpg.add_text("Translation", color=(255, 255, 0))
                    dpg.add_text("Source:")
                    dpg.add_text(
                        get_setting('translate', 'source_lang', 'Auto'),
                        color=(0, 255, 0),
                        tag="trans_source_display"
                    )
                    dpg.add_text("Target:")
                    dpg.add_text(
                        get_setting('translate', 'target_lang', 'None'),
                        color=(0, 255, 0),
                        tag="trans_target_display"
                    )

    def _create_credential_inputs(self, engine_name: str):
        """Create credential input fields for an engine"""
        if not engine_name:
            return
        
        engine_info = self.tts_mgr.engines[engine_name]
        if not engine_info['requires_credentials']:
            return

        # Clear existing items in credentials container
        dpg.delete_item("credentials_container", children_only=True)

        # Add new items inside the container
        with dpg.group(parent="credentials_container"):
            dpg.add_text("Credentials")
            for field in engine_info['credential_fields']:
                if field.field_type == "file":
                    dpg.add_button(
                        label=f"Select {field.label}",
                        callback=lambda: self._file_dialog_callback(field.name)
                    )
                    dpg.add_text("", tag=f"file_path_{field.name}")
                elif field.field_type == "region":
                    dpg.add_combo(
                        items=["eastus", "westus", "northeurope"],  # Add more as needed
                        label=field.label,
                        tag=f"input_{field.name}"
                    )
                else:  # text input
                    dpg.add_input_text(
                        label=field.label,
                        tag=f"input_{field.name}",
                        password=True
                    )

            dpg.add_button(
                label="Save Credentials",
                width=180,
                callback=self._on_save_credentials
            )

    def _on_engine_selected(self, sender, app_data):
        """Handle engine selection"""
        # Update credential inputs
        self._create_credential_inputs(app_data)

        # Clear and update voice table
        dpg.delete_item("voice_table_container", children_only=True)
        create_voice_table(self.tts_mgr, app_data)

    def _on_save_credentials(self, sender, app_data):
        """Handle saving credentials"""
        pass  # TODO: Implement credential saving

    def _create_translation_tab(self):
        with dpg.tab(label="Translation"):
            create_translation_tab(self.translation_mgr)

    def _create_settings_tab(self):
        with dpg.tab(label="Application Settings"):
            create_settings_tab()

    def _save_all_settings(self):
        """Save all settings to config file"""
        try:
            # Get values from UI
            settings = {
                'App': {
                    'collectstats': str(dpg.get_value("collect_stats"))
                },
                'appCache': {
                    'threshold': str(dpg.get_value("cache_threshold"))
                },
                'translate': {
                    'no_translate': str(not dpg.get_value("translate_enabled")),
                    'overwrite_pasteboard': str(dpg.get_value("overwrite_pasteboard")),
                    'bypass_tts': str(dpg.get_value("bypass_tts"))
                }
            }

            # Save to config file
            import configparser
            config = configparser.ConfigParser()
            
            # Read existing config to preserve other settings
            config.read('settings.cfg')
            
            # Update with new values
            for section, values in settings.items():
                if not config.has_section(section):
                    config.add_section(section)
                for key, value in values.items():
                    config.set(section, key, value)
            
            # Write to file
            with open('settings.cfg', 'w') as f:
                config.write(f)
            
            show_success_dialog("Settings saved successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to save settings: {e}")
            show_error_dialog(f"Failed to save settings: {str(e)}")

    def _discard_changes(self):
        """Reload settings from config file"""
        try:
            # Reload values from config
            dpg.set_value("collect_stats", get_setting('App', 'collectstats', True))
            dpg.set_value("cache_threshold", get_setting('appCache', 'threshold', 7))
            dpg.set_value("translate_enabled", get_translate_setting())
            
            show_info_dialog("Changes discarded")
            
        except Exception as e:
            self.logger.error(f"Failed to discard changes: {e}")
            show_error_dialog(f"Failed to reload settings: {str(e)}")

    def _file_dialog_callback(self, field_name: str) -> None:
        """Handle file dialog selection"""
        try:
            # Open file dialog
            file_path = dpg.add_file_dialog(
                label="Select File",
                callback=lambda s, a: self._on_file_selected(field_name, a['file_path_name']),
                modal=True
            )
        except Exception as e:
            self.logger.error(f"Failed to open file dialog: {e}")
            show_error_dialog(f"Failed to open file dialog: {str(e)}")

    def _on_file_selected(self, field_name: str, file_path: str) -> None:
        """Handle file selection"""
        try:
            dpg.set_value(f"file_path_{field_name}", file_path)
        except Exception as e:
            self.logger.error(f"Failed to set file path: {e}")
            show_error_dialog(f"Failed to set file path: {str(e)}")
