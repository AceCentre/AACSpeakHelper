# File: main.py
import dearpygui.dearpygui as dpg
from config_manager import ConfigManager
from logger import setup_logging


def main() -> None:
    """Main entry point for the application"""
    # Setup logging first
    setup_logging()
    
    # Initialize DearPyGui
    dpg.create_context()
    
    # Create config manager instance
    config = ConfigManager()
    config.create_main_window()
    
    # Setup viewport with proper size and theme
    dpg.create_viewport(
        title="AACSpeakHelper Config",
        width=1000,
        height=800,
        min_width=800,
        min_height=600
    )
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(config.window_tag, True)
    dpg.start_dearpygui()


if __name__ == "__main__":
    main()
