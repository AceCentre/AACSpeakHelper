# File: ui_components.py
from typing import Callable, Optional
import dearpygui.dearpygui as dpg
from language_manager import LanguageManager
from tts_manager import TTSManager
import logging
from pathlib import Path
from translation_manager import TranslationManager
import configparser
import os


def create_voice_table(tts_mgr: TTSManager, engine_name: str) -> None:
    """Create a table displaying voices for the selected engine"""
    logger = logging.getLogger(__name__)
    
    # Clear existing table
    if dpg.does_item_exist("voice_table_container"):
        dpg.delete_item("voice_table_container", children_only=True)
    
    voices = tts_mgr.get_voices(engine_name)
    logger.debug(f"Got {len(voices)} voices for {engine_name}")
    if voices:
        # Log first voice structure to see format
        logger.debug(f"First voice structure: {voices[0]}")
    
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
        dpg.add_table_column(label="Actions", width_fixed=True, width=150)

        if not voices:
            with dpg.table_row():
                if engine_name not in tts_mgr.clients:
                    dpg.add_text("Engine not initialized - credentials needed")
                else:
                    dpg.add_text("No voices available")
            return

        # Get current active voice
        active_voice = get_setting('tts', 'voice_id', '')
        active_engine = get_setting('tts', 'engine', '')

        for voice in voices:
            with dpg.table_row():
                # Get voice ID based on engine
                if engine_name == "Google TTS":
                    # Google uses language-Voice Name format
                    lang = voice.get('language_code', '')
                    name = voice.get('name', '')
                    voice_id = f"{lang}-{name}"
                else:
                    voice_id = voice.get('id', voice.get('name', 'Unknown'))
                
                logger.debug(f"Processing voice: {voice_id} with data: {voice}")
                
                # Display name
                display_name = voice.get('name', 'Unknown')
                if engine_name == "Google TTS":
                    display_name = f"{voice.get('name', 'Unknown')} ({voice.get('ssml_gender', 'N/A')})"
                dpg.add_text(display_name)
                
                # Display language
                lang = voice.get('language_code' if engine_name == "Google TTS" else 'language', 'Unknown')
                try:
                    if lang.lower() != 'unknown':
                        lang_name = LanguageManager.get_language_name(lang)
                        dpg.add_text(f"{lang_name} ({lang})")
                    else:
                        dpg.add_text(lang)
                except Exception as e:
                    logger.debug(f"Could not get language name for {lang}: {e}")
                    dpg.add_text(lang)
                
                # Display gender
                gender = voice.get('ssml_gender' if engine_name == "Google TTS" else 'gender', 'N/A')
                dpg.add_text(gender)
                
                with dpg.group(horizontal=True):
                    # Preview button
                    dpg.add_button(
                        label="Preview",
                        callback=lambda s, a, u=(engine_name, voice_id, tts_mgr): 
                            preview_voice(u[2], u[0], u[1]),
                        user_data=(engine_name, voice_id, tts_mgr)
                    )
                    
                    # Select button - highlighted if this is the active voice
                    is_active = (engine_name == active_engine and str(voice_id) == str(active_voice))
                    dpg.add_button(
                        label="Select" if not is_active else "Active",
                        callback=lambda s, a, u=(engine_name, voice_id, tts_mgr): 
                            set_active_voice(u[0], u[1], u[2]),
                        user_data=(engine_name, voice_id, tts_mgr),
                        enabled=not is_active
                    )
                    if is_active:
                        with dpg.theme() as active_theme:
                            with dpg.theme_component(dpg.mvButton):
                                dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 150, 0))
                        dpg.bind_item_theme(dpg.last_item(), active_theme)


def create_callback(
    func: Callable, tts_mgr: TTSManager, engine_name: str, voice_id: str
) -> Callable:
    """Create a callback with fixed parameters"""
    return lambda: func(tts_mgr, engine_name, voice_id)


def show_success_dialog(message: str) -> None:
    """Show a success dialog"""
    with dpg.window(label="Success", modal=True, no_close=False):
        dpg.add_text(message)
        dpg.add_button(label="OK", callback=lambda: dpg.delete_item(dpg.last_container()))


def show_error_dialog(message: str) -> None:
    """Show an error dialog"""
    with dpg.window(label="Error", modal=True, no_close=False):
        dpg.add_text(message)
        dpg.add_button(label="OK", callback=lambda: dpg.delete_item(dpg.last_container()))


def show_info_dialog(message: str) -> None:
    """Show an info dialog"""
    with dpg.window(label="Info", modal=True, no_close=False):
        dpg.add_text(message)
        dpg.add_button(label="OK", callback=lambda: dpg.delete_item(dpg.last_container()))


def preview_voice(tts_mgr: TTSManager, engine_name: str, voice_id: str) -> None:
    """Preview a voice"""
    try:
        if not voice_id:
            show_error_dialog("No voice selected")
            return
            
        if not engine_name:
            show_error_dialog("No engine selected")
            return
            
        tts_mgr.preview_voice(engine_name, voice_id)
    except Exception as e:
        logging.error(f"Failed to preview voice {voice_id}: {e}", exc_info=True)
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

    # Add result text area
    dpg.add_text("Translation Result:")
    dpg.add_text("", tag="translation_result")  # Create empty text widget for results

    # Test translation section
    dpg.add_text("Test Translation")
    dpg.add_input_text(
        multiline=True,
        height=100,
        tag="test_input",
        default_value="Hello, this is a test translation."
    )
    dpg.add_button(
        label="Test",
        callback=lambda: test_translation(translation_mgr)
    )


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


def set_result_text(tag: str, text: str) -> None:
    """Safely set text for a widget"""
    try:
        if dpg.does_item_exist(tag):
            dpg.set_value(tag, text)
        else:
            logging.error(f"Widget {tag} does not exist")
    except Exception as e:
        logging.error(f"Failed to set text for {tag}: {e}")


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
            set_result_text("translation_result", "Credentials saved successfully")
        else:
            set_result_text("translation_result", "Failed to initialize translator")
            
    except Exception as e:
        set_result_text("translation_result", f"Failed to save credentials: {str(e)}")
        logging.error(f"Failed to save translation credentials: {e}")


def save_translate_setting(enabled: bool) -> None:
    """Save translate setting to config file"""
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    
    if not config.has_section('translate'):
        config.add_section('translate')
    
    config.set('translate', 'no_translate', str(not enabled))
    
    with open('settings.cfg', 'w') as f:
        config.write(f)


def get_translate_setting() -> bool:
    """Get the translate setting"""
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    try:
        return not config.getboolean('translate', 'no_translate')
    except:
        return True


def create_settings_tab() -> None:
    """Create the application settings tab"""
    # Stats collection
    dpg.add_checkbox(
        label="Allow The Application to Collecting Stats",
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
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    
    if not config.has_section(section):
        config.add_section(section)
    
    config.set(section, key, value)
    
    with open('settings.cfg', 'w') as f:
        config.write(f)


def get_setting(section: str, key: str, default: any) -> any:
    """Get a setting from the config file"""
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


def set_active_voice(engine_name: str, voice_id: str, tts_mgr: TTSManager) -> None:
    """Set the active voice and save to settings"""
    try:
        # Save to config file
        config = configparser.ConfigParser()
        config.read('settings.cfg')
        
        if not config.has_section('tts'):
            config.add_section('tts')
            
        # Convert all values to strings
        config.set('tts', 'engine', str(engine_name))
        config.set('tts', 'voice_id', str(voice_id))
        
        # Get voice name for display
        voice_name = "Unknown"
        voices = tts_mgr.get_voices(engine_name)
        for voice in voices:
            # Handle different voice ID formats per engine
            if engine_name == "Google TTS":
                # Reconstruct Google voice ID
                lang = voice.get('language_code', '')
                name = voice.get('name', '')
                current_voice_id = f"{lang}-{name}"
                if str(current_voice_id) == str(voice_id):
                    voice_name = f"{voice.get('name', 'Unknown')} ({voice.get('ssml_gender', 'N/A')})"
                    break
            else:
                if str(voice.get('id')) == str(voice_id):
                    voice_name = str(voice.get('name', 'Unknown'))
                    break
                
        config.set('tts', 'voice_name', voice_name)
        
        with open('settings.cfg', 'w') as f:
            config.write(f)
            
        # Update display
        for tab in ["tts", "translation", "settings"]:
            if dpg.does_item_exist(f"active_engine_display_{tab}"):
                dpg.set_value(f"active_engine_display_{tab}", engine_name)
            if dpg.does_item_exist(f"active_voice_display_{tab}"):
                dpg.set_value(f"active_voice_display_{tab}", voice_name)
            
        # Refresh voice table to show new active voice
        create_voice_table(tts_mgr, engine_name)
        
        show_success_dialog(f"Active voice set to {voice_name}")
        
    except Exception as e:
        logging.error(f"Failed to set active voice: {e}", exc_info=True)
        show_error_dialog(f"Failed to set active voice: {str(e)}")


def create_current_settings_panel(tab_name: str = "") -> None:
    """Create the current settings panel that shows on all tabs"""
    with dpg.child_window(width=250, border=True):
        dpg.add_text("Current Settings", color=(255, 255, 0))
        dpg.add_separator()
        
        # Active TTS Engine
        dpg.add_text("TTS Engine:")
        dpg.add_text(
            get_setting('tts', 'engine', 'None'),
            color=(0, 255, 0),
            tag=f"active_engine_display_{tab_name}"  # Make tag unique
        )
        
        # Active Voice
        dpg.add_text("Voice:")
        dpg.add_text(
            get_setting('tts', 'voice_name', 'None'),
            color=(0, 255, 0),
            tag=f"active_voice_display_{tab_name}"  # Make tag unique
        )
        
        # Translation Settings
        dpg.add_separator()
        dpg.add_text("Translation", color=(255, 255, 0))
        dpg.add_text("Source:")
        dpg.add_text(
            get_setting('translate', 'source_lang', 'Auto'),
            color=(0, 255, 0),
            tag=f"trans_source_display_{tab_name}"  # Make tag unique
        )
        dpg.add_text("Target:")
        dpg.add_text(
            get_setting('translate', 'target_lang', 'None'),
            color=(0, 255, 0),
            tag=f"trans_target_display_{tab_name}"  # Make tag unique
        )
