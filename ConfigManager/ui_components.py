# File: ui_components.py
from typing import Callable
import dearpygui.dearpygui as dpg
from language_manager import LanguageManager
from tts_manager import TTSManager
import logging
from pathlib import Path


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
