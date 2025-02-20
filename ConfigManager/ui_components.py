# File: ui_components.py
from typing import Callable
import dearpygui.dearpygui as dpg
from language_manager import LanguageManager
from tts_manager import TTSManager


def create_voice_table(tts_mgr: TTSManager, engine_name: str) -> None:
    """Create a table displaying voices for the selected engine"""
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
        width=-1
    ):
        # Add columns with specific widths
        dpg.add_table_column(label="Name", width_fixed=True, width=200)
        dpg.add_table_column(label="Language", width_fixed=True, width=150)
        dpg.add_table_column(label="Gender", width_fixed=True, width=100)
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
                    lang_name = LanguageManager.get_language_name(lang)
                    dpg.add_text(f"{lang_name} ({lang})")
                except Exception as e:
                    dpg.add_text(lang)
                dpg.add_text(voice.get('gender', 'N/A'))

                # Create unique tags for buttons
                button_tag = f"button_{engine_name}_{voice['id']}"
                
                if tts_mgr.requires_download(engine_name) and not voice.get('is_downloaded', False):
                    dpg.add_button(
                        label="Download",
                        width=90,
                        height=25,
                        tag=button_tag,
                        callback=create_callback(download_voice, tts_mgr, engine_name, voice['id'])
                    )
                else:
                    dpg.add_button(
                        label="Preview",
                        width=90,
                        height=25,
                        tag=button_tag,
                        callback=create_callback(preview_voice, tts_mgr, engine_name, voice['id'])
                    )


def create_callback(
    func: Callable, tts_mgr: TTSManager, engine_name: str, voice_id: str
) -> Callable:
    """Create a callback with fixed parameters"""
    return lambda: func(tts_mgr, engine_name, voice_id)


def preview_voice(tts_mgr: TTSManager, engine_name: str, voice_id: str) -> None:
    """Preview a voice"""
    try:
        tts_mgr.preview_voice(engine_name, voice_id)
    except Exception as e:
        dpg.show_error_dialog(message=str(e))


def download_voice(tts_mgr: TTSManager, engine_name: str, voice_id: str) -> None:
    """Download a voice model"""
    try:
        client = tts_mgr.clients[engine_name]
        if hasattr(client, 'download_model'):
            client.download_model(voice_id)
            create_voice_table(tts_mgr, engine_name)
    except Exception as e:
        dpg.show_error_dialog(message=str(e))
