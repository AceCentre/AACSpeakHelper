# File: config_manager.py
import logging
import dearpygui.dearpygui as dpg
from encryption import EncryptionManager
from credential_manager import CredentialManager
from tts_manager import TTSManager
from ui_components import create_voice_table

class ConfigManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.encryption = EncryptionManager()
        self.cred_mgr = CredentialManager(self.encryption)
        self.tts_mgr = TTSManager()
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

        # Load font
        with dpg.font_registry():
            default_font = dpg.add_font(
                "assets/AtkinsonHyperlegibleNext-Regular.ttf", 
                16
            )
            dpg.bind_font(default_font)

        # Load and set icon - using PNG instead of ICO
        try:
            width, height, channels, data = dpg.load_image("assets/configure.png")
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

            with dpg.tab_bar():
                self._create_tts_tab()
                self._create_translation_tab()

    def _create_tts_tab(self):
        with dpg.tab(label="TTS Engines"):
            with dpg.group(horizontal=True):
                # Engine selection on the left
                with dpg.group():
                    engine_names = self.tts_mgr.get_engine_names()
                    dpg.add_combo(
                        items=engine_names,
                        label="Select Engine",
                        width=200,
                        callback=self._on_engine_selected,
                        default_value=engine_names[0] if engine_names else ""
                    )
                    
                    dpg.add_spacer(height=10)
                    
                    # Create a permanent container for credentials
                    dpg.add_group(tag="credentials_container")
                    self._create_credential_inputs(engine_names[0] if engine_names else None)

            dpg.add_spacer(height=10)

            # Voice table container
            with dpg.child_window(tag="voice_table_container", border=True):
                if engine_names:
                    engine_name = engine_names[0]
                    if engine_name == "SherpaOnnx":
                        self.tts_mgr.initialize_engine(engine_name, None)
                        create_voice_table(self.tts_mgr, engine_name)

    def _create_credential_inputs(self, engine_name: str):
        """Create credential input fields based on engine requirements"""
        if not engine_name:
            return

        # Clear existing items in credentials container
        dpg.delete_item("credentials_container", children_only=True)

        # Add new items inside the container
        with dpg.group(parent="credentials_container"):
            config = self.tts_mgr.engines[engine_name]
            if not config.requires_credentials:
                dpg.add_text("No credentials required")
                return

            dpg.add_text("Credentials")
            for field in config.credential_fields:
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
        
        # Only try to show voices for SherpaOnnx or engines with credentials
        if app_data == "SherpaOnnx":
            self.tts_mgr.initialize_engine(app_data, None)
            create_voice_table(self.tts_mgr, app_data)

    def _on_save_credentials(self, sender, app_data):
        """Handle saving credentials"""
        pass  # TODO: Implement credential saving

    def _create_translation_tab(self):
        with dpg.tab(label="Translation"):
            # Translation tab implementation
            pass
