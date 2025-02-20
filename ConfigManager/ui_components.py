# File: ui_components.py
from typing import Callable
import dearpygui.dearpygui as dpg
from language_manager import LanguageManager
from tts_manager import TTSManager
import logging
from pathlib import Path
from translation_manager import TranslationManager


def create_voice_table(tts_mgr: TTSManager, engine_name: str) -> None:
    """Create a table displaying voices for the selected engine"""
    logger = logging.getLogger(__name__)
    
    # Clear existing table
    if dpg.does_item_exist("voice_table_container"):
        dpg.delete_item("voice_table_container", children_only=True)
    
    with dpg.table(
        header_row=True,
        policy=dpg.mvTable_SizingStretchProp,
        parent="voice_table_container",
        borders_innerH=True,
        borders_outerH=True,
        borders_innerV=True,
        borders_outerV=True,
        row_background=True,
        resizable=True,
        width=-1,
        tag="voice_table"
    ):
        # Add columns
        dpg.add_table_column(label="Name", width_fixed=True, width=200)
        dpg.add_table_column(label="Language", width_fixed=True, width=150)
        dpg.add_table_column(label="Gender", width_fixed=True, width=100)
        dpg.add_table_column(label="Status", width_fixed=True, width=100)
        dpg.add_table_column(label="Actions", width_fixed=True, width=100)

        voices = tts_mgr.get_voices(engine_name)
        
        if not voices:
            with dpg.table_row():
                if tts_mgr.engines[engine_name].requires_credentials:
                    dpg.add_text("No voices available - credentials needed")
                else:
                    dpg.add_text("No voices available")
            return

        for voice in voices:
            with dpg.table_row():
                dpg.add_text(voice.get('name', 'Unknown'))
                lang = voice.get('language', 'Unknown')
                try:
                    if lang.lower() != 'unknown':
                        lang_name = LanguageManager.get_language_name(lang)
                        dpg.add_text(f"{lang_name} ({lang})")
                    else:
                        dpg.add_text(lang)
                except Exception as e:
                    logger.debug(f"Could not get language name for {lang}: {e}")
                    dpg.add_text(lang)
                dpg.add_text(voice.get('gender', 'N/A'))

                # Status and action buttons
                status_tag = f"status_{engine_name}_{voice['id']}"
                button_tag = f"button_{engine_name}_{voice['id']}"
                
                if engine_name == "SherpaOnnx":
                    # Check if model exists without triggering download
                    client = tts_mgr.clients[engine_name]
                    try:
                        # Use client's base directory
                        voice_dir = client._base_dir / voice['id']
                        model_file = voice_dir / "model.onnx"
                        tokens_file = voice_dir / "tokens.txt"
                        
                        model_exists = (
                            model_file.exists() and 
                            model_file.stat().st_size > 1024*1024 and
                            tokens_file.exists() and 
                            tokens_file.stat().st_size > 0
                        )
                        
                        # Status column
                        if model_exists:
                            dpg.add_text("Downloaded", tag=status_tag, color=(0, 255, 0))
                            dpg.add_button(
                                label="Preview",
                                width=90,
                                height=25,
                                tag=button_tag,
                                callback=create_callback(
                                    preview_voice, 
                                    tts_mgr, 
                                    engine_name, 
                                    voice['id']
                                )
                            )
                        else:
                            dpg.add_text("Not Downloaded", tag=status_tag, color=(255, 165, 0))
                            dpg.add_button(
                                label="Download",
                                width=90,
                                height=25,
                                tag=button_tag,
                                callback=create_callback(
                                    download_voice, 
                                    tts_mgr, 
                                    engine_name, 
                                    voice['id']
                                )
                            )
                    except Exception as e:
                        logger.error(f"Error checking model files: {e}")
                elif tts_mgr.requires_download(engine_name):
                    # Handle other downloadable engines
                    if not voice.get('is_downloaded', False):
                        dpg.add_button(
                            label="Download",
                            width=90,
                            height=25,
                            tag=button_tag,
                            callback=create_callback(
                                download_voice, 
                                tts_mgr, 
                                engine_name, 
                                voice['id']
                            )
                        )
                else:
                    # Non-downloadable engines just get preview
                    dpg.add_button(
                        label="Preview",
                        width=90,
                        height=25,
                        tag=button_tag,
                        callback=create_callback(
                            preview_voice, 
                            tts_mgr, 
                            engine_name, 
                            voice['id']
                        )
                    )


def create_callback(
    func: Callable, tts_mgr: TTSManager, engine_name: str, voice_id: str
) -> Callable:
    """Create a callback with fixed parameters"""
    return lambda: func(tts_mgr, engine_name, voice_id)


def show_success_dialog(message: str):
    """Show a success dialog"""
    def _create_dialog():
        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()
        window_width = 400
        window_height = 100
        
        window_tag = f"success_dialog_{dpg.generate_uuid()}"
        
        with dpg.window(
            label="Success",
            modal=True,
            no_close=False,
            width=window_width,
            height=window_height,
            pos=[
                viewport_width//2 - window_width//2,
                viewport_height//2 - window_height//2
            ],
            tag=window_tag
        ):
            dpg.add_text(message, color=(0, 255, 0))
            dpg.add_button(
                label="OK",
                width=75,
                callback=lambda: dpg.delete_item(window_tag)
            )
    
    dpg.split_frame()  # Wait for next frame
    _create_dialog()


def show_error_dialog(message: str):
    """Show an error dialog"""
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()
    window_width = 400
    window_height = 100
    
    # Create unique tag for window
    window_tag = f"error_dialog_{dpg.generate_uuid()}"
    
    with dpg.window(
        label="Error",
        modal=True,
        no_close=False,
        width=window_width,
        height=window_height,
        pos=[
            viewport_width//2 - window_width//2,
            viewport_height//2 - window_height//2
        ],
        tag=window_tag
    ):
        dpg.add_text(message, color=(255, 0, 0))
        dpg.add_button(
            label="OK",
            width=75,
            callback=lambda: dpg.delete_item(window_tag)
        )


def preview_voice(tts_mgr: TTSManager, engine_name: str, voice_id: str) -> None:
    """Preview a voice"""
    try:
        tts_mgr.preview_voice(engine_name, voice_id)
    except Exception as e:
        show_error_dialog(str(e))


def download_voice(tts_mgr: TTSManager, engine_name: str, voice_id: str) -> None:
    """Queue a voice model download"""
    logger = logging.getLogger(__name__)
    
    try:
        # Create download progress window
        with dpg.window(
            label="Download Queue",
            modal=True,
            no_close=True,
            width=300,
            height=150,
            pos=[
                dpg.get_viewport_width()//2 - 150,
                dpg.get_viewport_height()//2 - 75
            ]
        ) as progress_window:
            dpg.add_text(f"Downloading {voice_id}...")
            dpg.add_text(f"Queue size: {len(tts_mgr.download_queue) + 1}")
            dpg.add_loading_indicator()
            
            try:
                # Queue and wait for download
                tts_mgr.queue_download(engine_name, voice_id)
                while tts_mgr.downloading:
                    dpg.render_dearpygui_frame()  # Keep UI responsive
                
                # Close progress and refresh on success
                dpg.delete_item(progress_window)
                show_success_dialog(
                    f"Successfully downloaded voice model:\n{voice_id}"
                )
                create_voice_table(tts_mgr, engine_name)
                
            except Exception as e:
                # Clean up on error
                dpg.delete_item(progress_window)
                logger.error(f"Download failed for {voice_id}: {e}")
                show_error_dialog(f"Failed to download voice: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error during download setup: {e}")
        show_error_dialog(f"Error during download: {str(e)}")


def create_translation_tab(translation_mgr: TranslationManager) -> None:
    """Create the translation configuration tab"""
    # Main translate toggle
    dpg.add_checkbox(
        label="Translate",
        callback=lambda s, a: save_translate_setting(a),
        default_value=get_translate_setting(),
        tag="translate_enabled"
    )
    
    dpg.add_text("Translate Settings")
    
    # Additional settings
    dpg.add_checkbox(
        label="Overwrite Pasteboard",
        default_value=True,
        tag="overwrite_pasteboard"
    )
    
    dpg.add_checkbox(
        label="Bypass TTS",
        default_value=False,
        tag="bypass_tts"
    )
    
    # Provider and language selection
    dpg.add_combo(
        items=list(translation_mgr.translators.keys()),
        label="Provider",
        callback=lambda s, a: on_provider_selected(translation_mgr, a),
        width=200,
        tag="translation_provider",
        default_value="Google"  # Since we initialize it by default
    )
    
    dpg.add_combo(
        label="Writing Language",
        items=["Auto"],  # Will be populated when provider initialized
        width=200,
        tag="source_language"
    )
    
    dpg.add_combo(
        label="Target Language",
        items=["English"],  # Will be populated when provider initialized
        width=200,
        tag="target_language"
    )
    
    # Credentials container (hidden by default for Google)
    with dpg.group(tag="translation_credentials"):
        pass


def on_provider_selected(translation_mgr: TranslationManager, provider: str) -> None:
    """Handle translation provider selection"""
    # Clear existing credentials
    dpg.delete_item("translation_credentials", children_only=True)
    
    config = translation_mgr.translators[provider]
    
    # Add credential fields if needed
    with dpg.group(parent="translation_credentials"):
        if config.requires_api_key:
            dpg.add_input_text(
                label="API Key",
                password=True,
                tag=f"api_key_{provider}",
                width=300
            )
        if config.base_url:
            dpg.add_input_text(
                label="API URL",
                default_value=config.base_url,
                tag=f"base_url_{provider}",
                width=300
            )
        if config.requires_api_key or config.base_url:
            dpg.add_button(
                label="Save Credentials",
                callback=lambda: save_translation_credentials(translation_mgr, provider),
                width=200
            )
    
    # Update language lists if provider is initialized
    if provider in translation_mgr.instances:
        try:
            languages = translation_mgr.get_supported_languages(provider)
            dpg.configure_item(
                "source_language",
                items=["Auto"] + [l["code"] for l in languages]
            )
            dpg.configure_item(
                "target_language",
                items=[l["code"] for l in languages]
            )
        except Exception as e:
            logging.error(f"Failed to get languages for {provider}: {e}")


def test_translation(translation_mgr: TranslationManager) -> None:
    """Test the selected translation provider"""
    provider = dpg.get_value("translation_provider")
    
    try:
        # Get test text
        text = dpg.get_value("test_input")
        if not text:
            text = "Hello, this is a test translation."
            dpg.set_value("test_input", text)
            
        # Get languages
        source = dpg.get_value("source_language")
        target = dpg.get_value("target_language")
        
        # Translate
        result = translation_mgr.translate(
            text,
            provider,
            source_lang=source if source != "Auto" else "auto",
            target_lang=target
        )
        
        # Show result
        dpg.set_value("translation_result", result)
        
    except Exception as e:
        dpg.set_value("translation_result", f"Translation failed: {str(e)}")
        logging.error(f"Translation test failed: {e}")


def save_translation_credentials(translation_mgr: TranslationManager, provider: str) -> None:
    """Save credentials for a translation provider"""
    try:
        config = translation_mgr.translators[provider]
        kwargs = {}
        
        if config.requires_api_key:
            kwargs['api_key'] = dpg.get_value(f"api_key_{provider}")
        if config.base_url:
            kwargs['base_url'] = dpg.get_value(f"base_url_{provider}")
            
        # Initialize with new credentials
        if translation_mgr.initialize_translator(provider, **kwargs):
            # Update language lists
            languages = translation_mgr.get_supported_languages(provider)
            dpg.configure_item(
                "source_language",
                items=["Auto"] + [l["code"] for l in languages]
            )
            dpg.configure_item(
                "target_language",
                items=[l["code"] for l in languages]
            )
            dpg.set_value("translation_result", "Credentials saved successfully")
        else:
            dpg.set_value("translation_result", "Failed to initialize translator")
            
    except Exception as e:
        dpg.set_value("translation_result", f"Failed to save credentials: {str(e)}")
        logging.error(f"Failed to save translation credentials: {e}")


def save_translate_setting(enabled: bool) -> None:
    """Save translate setting to config file"""
    import configparser
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    
    if not config.has_section('translate'):
        config.add_section('translate')
    
    config.set('translate', 'no_translate', str(not enabled))
    
    with open('settings.cfg', 'w') as f:
        config.write(f)


def get_translate_setting() -> bool:
    """Get translate setting from config file"""
    import configparser
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    
    try:
        return not config.getboolean('translate', 'no_translate')
    except:
        return True  # Default to enabled if setting doesn't exist


def create_settings_tab() -> None:
    """Create the application settings tab"""
    # Stats collection
    dpg.add_checkbox(
        label="Allow The Application to Collecting Stats",
        callback=lambda s, a: save_setting('App', 'collectstats', str(a)),
        default_value=get_setting('App', 'collectstats', True),
        tag="collect_stats"
    )
    
    dpg.add_spacer(height=10)
    
    # Cache settings
    dpg.add_text("Application Cache Threshold:")
    with dpg.group(horizontal=True):
        dpg.add_input_int(
            width=100,
            default_value=get_setting('appCache', 'threshold', 7),
            callback=lambda s, a: save_setting('appCache', 'threshold', str(a)),
            tag="cache_threshold"
        )
        dpg.add_text("day(s)")
    
    dpg.add_spacer(height=10)
    
    # Application path
    dpg.add_text("Application Path:")
    with dpg.group(horizontal=True):
        dpg.add_input_text(
            width=400,
            readonly=True,
            tag="app_path"
        )
        dpg.add_button(
            label="Copy Path of Main app",
            callback=lambda: dpg.set_clipboard_text(dpg.get_value("app_path"))
        )
    
    dpg.add_spacer(height=10)
    
    # Cache management buttons
    with dpg.group(horizontal=True):
        dpg.add_button(
            label="Clear Cache",
            callback=clear_cache,
            width=150
        )
        dpg.add_button(
            label="Open Cache",
            callback=open_cache,
            width=150
        )


def save_setting(section: str, key: str, value: str) -> None:
    """Save a setting to the config file"""
    import configparser
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    
    if not config.has_section(section):
        config.add_section(section)
    
    config.set(section, key, value)
    
    with open('settings.cfg', 'w') as f:
        config.write(f)


def get_setting(section: str, key: str, default: any) -> any:
    """Get a setting from the config file"""
    import configparser
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    
    try:
        if key in ['collectstats']:
            return config.getboolean(section, key)
        elif key in ['threshold']:
            return config.getint(section, key)
        else:
            return config.get(section, key)
    except:
        return default


def clear_cache() -> None:
    """Clear the application cache"""
    # TODO: Implement cache clearing
    show_info_dialog("Cache cleared")


def open_cache() -> None:
    """Open the cache directory"""
    import os
    import platform
    import subprocess
    
    # TODO: Get actual cache path
    cache_path = os.path.expanduser("~/AppData/Local/Ace Centre/AACSpeakHelper/cache")
    
    if platform.system() == "Windows":
        os.startfile(cache_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", cache_path])
    else:  # Linux
        subprocess.run(["xdg-open", cache_path])
