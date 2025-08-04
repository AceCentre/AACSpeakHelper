#!/usr/bin/env python3
"""
GUI Configuration and Testing Tool for AACSpeakHelper
Provides a user-friendly graphical interface to configure and test TTS engines.
"""

import sys
import os
import configparser
import tempfile
import re
import logging
from pathlib import Path

try:
    from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                                   QWidget, QPushButton, QLabel, QComboBox, QLineEdit,
                                   QTextEdit, QMessageBox, QInputDialog, QFileDialog,
                                   QFormLayout, QGroupBox, QProgressBar)
    from PySide6.QtCore import Qt, QThread, Signal as pyqtSignal
except ImportError:
    print("Error: PySide6 is required. Install with: uv add PySide6")
    sys.exit(1)

# Import existing modules
try:
    from cli_config_creator import TTS_ENGINES, get_config_dir
    import tts_utils
    import utils
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Make sure you're running from the AACSpeakHelper directory")
    sys.exit(1)


class VoiceFetchWorker(QThread):
    """Worker thread for fetching voices from TTS APIs using existing tts_utils"""
    voices_fetched = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, temp_config_path):
        super().__init__()
        self.temp_config_path = temp_config_path

    def run(self):
        """Fetch voices in background thread using tts_utils.speak with list_voices=True"""
        try:
            # Load the temporary config file
            temp_config = configparser.ConfigParser()
            temp_config.read(self.temp_config_path)

            # Get paths using utils.get_paths
            config_path, audio_files_path = utils.get_paths(self.temp_config_path)

            # Add App section with required paths
            if "App" not in temp_config:
                temp_config["App"] = {}
            temp_config["App"]["config_path"] = config_path
            temp_config["App"]["audio_files_path"] = audio_files_path

            # Create args dictionary
            args = {
                "config": self.temp_config_path,
                "listvoices": True,
                "preview": False,
                "style": "",
                "styledegree": None,
            }

            # Store original state
            original_config = utils.config if hasattr(utils, 'config') else None
            original_config_path = utils.config_path if hasattr(utils, 'config_path') else None
            original_audio_path = utils.audio_files_path if hasattr(utils, 'audio_files_path') else None

            # Initialize utils with proper format
            utils.init(temp_config, args)

            # Initialize tts_utils with utils
            tts_utils.init(utils)

            # Call speak with list_voices=True to get voices
            tts_utils.speak(text="", list_voices=True)

            # Get the voices from the global variable
            voices_result = tts_utils.voices

            # Restore original state
            if original_config and original_config_path and original_audio_path:
                utils.config = original_config
                utils.config_path = original_config_path
                utils.audio_files_path = original_audio_path
                tts_utils.utils = utils

            if voices_result:
                self.voices_fetched.emit(voices_result)
            else:
                self.error_occurred.emit("No voices found or credentials not configured")

        except Exception as e:
            self.error_occurred.emit(str(e))


class GUIConfigTester(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
        self.config_path = None
        self.temp_config_path = None
        self.current_engine = None

        # Initialize UI with reduced height (one-third smaller: 500 -> 330)
        self.setWindowTitle("AACSpeakHelper GUI Configuration & Testing Tool")
        self.setGeometry(100, 100, 600, 330)
        self.setMinimumSize(550, 300)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(8)  # Reduce spacing between sections

        # Engine selection
        engine_group = QGroupBox("TTS Engine Selection")
        engine_layout = QFormLayout(engine_group)

        self.engine_combo = QComboBox()
        self.populate_engine_combo()
        self.engine_combo.currentTextChanged.connect(self.on_engine_changed)
        engine_layout.addRow("Engine:", self.engine_combo)

        layout.addWidget(engine_group)

        # Configuration section
        config_group = QGroupBox("Configuration")
        config_layout = QVBoxLayout(config_group)

        self.config_form = QFormLayout()
        config_layout.addLayout(self.config_form)

        # Voice selection with dynamic fetching
        voice_layout = QVBoxLayout()

        # Voice combo and refresh button
        voice_controls = QHBoxLayout()
        self.voice_combo = QComboBox()
        self.voice_combo.setEditable(True)  # Allow manual input for engines without predefined voices
        voice_controls.addWidget(self.voice_combo)

        self.refresh_voices_btn = QPushButton("Fetch Voices")
        self.refresh_voices_btn.clicked.connect(self.fetch_dynamic_voices)
        voice_controls.addWidget(self.refresh_voices_btn)

        voice_layout.addLayout(voice_controls)

        # Progress bar for voice fetching
        self.voice_progress = QProgressBar()
        self.voice_progress.setVisible(False)
        self.voice_progress.setMaximumHeight(15)
        voice_layout.addWidget(self.voice_progress)

        self.config_form.addRow("Voice:", voice_layout)

        layout.addWidget(config_group)

        # Testing section
        test_group = QGroupBox("TTS Testing")
        test_layout = QVBoxLayout(test_group)

        self.test_text = QTextEdit()
        self.test_text.setPlainText("Hello, this is a test of the AACSpeakHelper TTS system.")
        self.test_text.setMaximumHeight(60)  # Reduced from 80 to 60
        test_layout.addWidget(QLabel("Test Text:"))
        test_layout.addWidget(self.test_text)

        # Test buttons
        button_layout = QHBoxLayout()

        play_btn = QPushButton("Play TTS")
        play_btn.clicked.connect(self.test_playback)
        button_layout.addWidget(play_btn)

        save_btn = QPushButton("Save as WAV")
        save_btn.clicked.connect(self.save_wav)
        button_layout.addWidget(save_btn)

        test_layout.addLayout(button_layout)
        layout.addWidget(test_group)

        # Status section
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        # Initialize worker thread
        self.voice_worker = None

        # Load current configuration
        self.load_current_config()

    def populate_engine_combo(self):
        """Populate engine combo box"""
        self.engine_combo.clear()
        for engine_id, engine_info in TTS_ENGINES.items():
            self.engine_combo.addItem(f"{engine_info['name']}", engine_id)

    def load_current_config(self):
        """Load current configuration as defaults"""
        default_config_path = os.path.join(get_config_dir(), "settings.cfg")
        if os.path.exists(default_config_path):
            self.config.read(default_config_path)
            self.config_path = default_config_path
            self.status_label.setText(f"Loaded defaults from: {default_config_path} (testing only - changes not saved)")

            # Set current engine in combo box
            current_engine = self.config.get("TTS", "engine", fallback="azureTTS")
            for i in range(self.engine_combo.count()):
                engine_id = self.engine_combo.itemData(i)
                if TTS_ENGINES[engine_id]["config_section"] == current_engine:
                    self.engine_combo.setCurrentIndex(i)
                    self.current_engine = engine_id
                    # Update the form to show credentials for the loaded engine
                    self.update_config_form()
                    self.refresh_static_voices()
                    break
        else:
            self.status_label.setText("No existing configuration found. Starting with defaults.")
            self.create_default_config()
    
    def create_default_config(self):
        """Create a default configuration"""
        # Use the same default creation logic as CLI tool
        from cli_config_creator import create_default_config
        create_default_config(self.config)
    
    def sanitize_filename(self, text):
        """Sanitize text for use as filename"""
        # Remove or replace invalid filename characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', text)
        # Limit length and remove extra spaces
        sanitized = sanitized.strip()[:50]
        return sanitized if sanitized else "test_audio"

    def validate_engine_selected(self):
        """Common validation to check if engine is selected"""
        if not self.current_engine:
            QMessageBox.warning(self, "No Engine Selected", "Please select a TTS engine first.")
            return False
        return True

    def validate_voice_configured(self):
        """Common validation to check if voice is configured"""
        if not self.current_engine:
            return False

        engine_info = TTS_ENGINES[self.current_engine]
        config_section = engine_info["config_section"]

        if not self.config.has_option(config_section, "voice_id"):
            QMessageBox.warning(self, "No Voice Selected",
                              f"Please select a voice for {engine_info['name']} first.")
            return False
        return True

    def validate_test_text(self):
        """Common validation to check if test text is provided"""
        text = self.test_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "No Text", "Please enter some text to test.")
            return False, None
        return True, text

    def show_error(self, title, message):
        """Common error display method"""
        QMessageBox.critical(self, title, message)

    def show_info(self, title, message):
        """Common info display method"""
        QMessageBox.information(self, title, message)

    def update_status(self, message):
        """Common status update method"""
        self.status_label.setText(message)

    def ensure_config_section(self, section):
        """Common method to ensure config section exists"""
        if not self.config.has_section(section):
            self.config.add_section(section)

    def on_engine_changed(self, engine_text):
        """Handle engine selection change"""
        if not engine_text:
            return

        # Find engine ID from combo box
        current_index = self.engine_combo.currentIndex()
        if current_index >= 0:
            engine_id = self.engine_combo.itemData(current_index)
            self.current_engine = engine_id

            # Update TTS section
            self.ensure_config_section("TTS")
            self.config.set("TTS", "engine", TTS_ENGINES[engine_id]["config_section"])

            # Update configuration form
            self.update_config_form()
            self.refresh_static_voices()

            self.update_status(f"Selected engine: {TTS_ENGINES[engine_id]['name']}")

            # Auto-fetch voices if credentials are already configured
            self.auto_fetch_voices_if_configured()

    def update_config_form(self):
        """Update configuration form based on selected engine"""
        # Clear existing form items (except voice which is handled separately)
        while self.config_form.rowCount() > 1:  # Keep voice row
            self.config_form.removeRow(1)

        if not self.current_engine:
            return

        engine_info = TTS_ENGINES[self.current_engine]
        config_section = engine_info["config_section"]

        # Ensure section exists
        self.ensure_config_section(config_section)

        # Add credential fields
        self.credential_fields = {}
        for field in engine_info["credential_fields"]:
            line_edit = QLineEdit()
            current_value = self.config.get(config_section, field, fallback="")
            line_edit.setText(current_value)

            # Use password mode for sensitive fields
            if "key" in field.lower() or "secret" in field.lower() or "token" in field.lower():
                line_edit.setEchoMode(QLineEdit.EchoMode.Password)

            # Connect to update config and trigger voice refresh when credentials change
            line_edit.textChanged.connect(
                lambda text, f=field, s=config_section: self.on_credential_changed(s, f, text)
            )

            self.credential_fields[field] = line_edit
            self.config_form.addRow(f"{field.title()}:", line_edit)

    def on_credential_changed(self, section, field, value):
        """Handle credential field changes and trigger voice refresh"""
        self.update_config_field(section, field, value)

        # Auto-fetch voices when credentials are updated (with small delay to avoid too many requests)
        if hasattr(self, '_credential_timer'):
            self._credential_timer.stop()

        from PySide6.QtCore import QTimer
        self._credential_timer = QTimer()
        self._credential_timer.setSingleShot(True)
        self._credential_timer.timeout.connect(self.auto_fetch_voices_if_configured)
        self._credential_timer.start(1000)  # 1 second delay

    def update_config_field(self, section, field, value):
        """Update configuration field (in memory only for testing)"""
        self.ensure_config_section(section)
        self.config.set(section, field, value)
        # Note: Changes are NOT saved to settings.cfg - this is a testing tool only

    def auto_fetch_voices_if_configured(self):
        """Auto-fetch voices if credentials are configured"""
        if not self.current_engine:
            return

        engine_info = TTS_ENGINES[self.current_engine]
        config_section = engine_info["config_section"]
        credential_fields = engine_info["credential_fields"]

        # Check if all required credentials are configured
        if credential_fields:
            all_configured = True
            for field in credential_fields:
                value = self.config.get(config_section, field, fallback="").strip()
                if not value:
                    all_configured = False
                    break

            if all_configured:
                self.fetch_dynamic_voices()

    def fetch_dynamic_voices(self):
        """Fetch voices dynamically from TTS API using existing tts_utils"""
        if not self.validate_engine_selected():
            return

        # Don't start new fetch if one is already running
        if self.voice_worker and self.voice_worker.isRunning():
            return

        # Show progress
        self.voice_progress.setVisible(True)
        self.voice_progress.setRange(0, 0)  # Indeterminate progress
        self.refresh_voices_btn.setEnabled(False)
        self.update_status("Fetching voices from API...")

        # Create temporary config for voice fetching
        temp_config = self.create_temp_config()

        # Start worker thread with temp config
        self.voice_worker = VoiceFetchWorker(temp_config)
        self.voice_worker.voices_fetched.connect(self.on_voices_fetched)
        self.voice_worker.error_occurred.connect(self.on_voice_fetch_error)
        self.voice_worker.start()

    def on_voices_fetched(self, voices):
        """Handle successfully fetched voices from tts_utils"""
        self.voice_progress.setVisible(False)
        self.refresh_voices_btn.setEnabled(True)

        if not voices:
            self.update_status("No voices found")
            return

        # Clear current voices and add fetched ones
        self.voice_combo.clear()

        # Get current voice to preserve selection
        engine_info = TTS_ENGINES[self.current_engine]
        config_section = engine_info["config_section"]
        current_voice = self.config.get(config_section, "voice_id", fallback="")

        current_index = -1

        # Handle different voice formats from TTS wrapper
        for i, voice in enumerate(voices):
            if hasattr(voice, '__dict__'):
                # Voice object with attributes
                voice_id = getattr(voice, 'id', getattr(voice, 'voice_id', getattr(voice, 'name', str(voice))))
                voice_name = getattr(voice, 'display_name', getattr(voice, 'name', voice_id))
                language = getattr(voice, 'language', getattr(voice, 'locale', ''))
                gender = getattr(voice, 'gender', '')

                # Create display text with additional info
                display_parts = [voice_name]
                if language:
                    display_parts.append(f"[{language}]")
                if gender:
                    display_parts.append(f"({gender})")
                display_text = " ".join(display_parts) + f" - {voice_id}"

            elif isinstance(voice, dict):
                # Dictionary format
                voice_id = voice.get('id', voice.get('voice_id', voice.get('name', str(voice))))
                voice_name = voice.get('display_name', voice.get('name', voice_id))
                language = voice.get('language', voice.get('locale', ''))
                gender = voice.get('gender', '')

                # Create display text with additional info
                display_parts = [voice_name]
                if language:
                    display_parts.append(f"[{language}]")
                if gender:
                    display_parts.append(f"({gender})")
                display_text = " ".join(display_parts) + f" - {voice_id}"

            else:
                # Simple string format
                voice_id = str(voice)
                display_text = voice_id

            self.voice_combo.addItem(display_text, voice_id)

            if voice_id == current_voice:
                current_index = i

        # Restore selection
        if current_index >= 0:
            self.voice_combo.setCurrentIndex(current_index)

        self.update_status(f"Fetched {len(voices)} voices from API")

    def on_voice_fetch_error(self, error_message):
        """Handle voice fetch errors"""
        self.voice_progress.setVisible(False)
        self.refresh_voices_btn.setEnabled(True)
        self.update_status(f"Voice fetch failed: {error_message}")

        # Fall back to static voices
        self.refresh_static_voices()

    def refresh_static_voices(self):
        """Refresh voice list with static/predefined voices"""
        if not self.current_engine:
            return

        engine_info = TTS_ENGINES[self.current_engine]
        config_section = engine_info["config_section"]
        voice_list = engine_info["voice_list"]

        self.voice_combo.clear()

        if voice_list:
            # Add predefined voices
            for name, voice_id in voice_list.items():
                self.voice_combo.addItem(f"{name} ({voice_id})", voice_id)

            # Set current voice if exists
            if self.config.has_option(config_section, "voice_id"):
                current_voice = self.config.get(config_section, "voice_id")
                for i in range(self.voice_combo.count()):
                    if self.voice_combo.itemData(i) == current_voice:
                        self.voice_combo.setCurrentIndex(i)
                        break
        else:
            # For engines without predefined voices, show current value
            if self.config.has_option(config_section, "voice_id"):
                current_voice = self.config.get(config_section, "voice_id")
                self.voice_combo.addItem(current_voice, current_voice)

        # Connect voice selection change (disconnect first to avoid duplicates)
        try:
            self.voice_combo.currentTextChanged.disconnect()
        except:
            pass
        self.voice_combo.currentTextChanged.connect(self.on_voice_changed)

    def on_voice_changed(self):
        """Handle voice selection change"""
        if not self.current_engine:
            return

        engine_info = TTS_ENGINES[self.current_engine]
        config_section = engine_info["config_section"]

        # Get voice ID from combo box or text
        current_index = self.voice_combo.currentIndex()
        if current_index >= 0:
            voice_id = self.voice_combo.itemData(current_index)
            if voice_id is None:  # Manual entry
                voice_id = self.voice_combo.currentText()
        else:
            voice_id = self.voice_combo.currentText()

        # Update configuration
        self.ensure_config_section(config_section)
        self.config.set(config_section, "voice_id", voice_id)

        self.update_status(f"Selected voice: {voice_id}")
    
    def test_playback(self):
        """Test TTS playback"""
        if not self.validate_engine_selected():
            return

        if not self.validate_voice_configured():
            return

        valid, text = self.validate_test_text()
        if not valid:
            return

        try:
            self.update_status("Testing TTS playback...")
            self.test_tts_playback(text)
            self.update_status("TTS test completed")
        except Exception as e:
            self.show_error("TTS Test Error", f"Error during TTS test:\n{str(e)}")
            self.update_status("TTS test failed")

    def save_wav(self):
        """Save TTS as WAV file"""
        if not self.validate_engine_selected():
            return

        if not self.validate_voice_configured():
            return

        valid, text = self.validate_test_text()
        if not valid:
            return

        # Get filename from user
        sanitized_text = self.sanitize_filename(text)
        default_filename = f"{sanitized_text}.wav"

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Audio File",
            default_filename,
            "WAV files (*.wav);;All files (*.*)"
        )

        if filename:
            try:
                self.update_status("Saving audio file...")
                self.save_as_wav_file(text, filename)
                self.update_status(f"Audio saved to: {filename}")
                self.show_info("Audio Saved", f"Audio saved successfully to:\n{filename}")
            except Exception as e:
                self.show_error("Save Error", f"Error saving audio file:\n{str(e)}")
                self.update_status("Audio save failed")
    
    def save_as_wav_file(self, text, filename):
        """Save TTS output as WAV file using existing tts_utils functionality"""
        # Create temporary config
        temp_config = self.create_temp_config()

        # Temporarily enable save_audio_file in config
        original_save_setting = self.config.get("TTS", "save_audio_file", fallback="True")
        self.config.set("TTS", "save_audio_file", "True")

        # Write updated config
        with open(temp_config, 'w') as f:
            self.config.write(f)

        try:
            # Load the temporary config file
            temp_config_obj = configparser.ConfigParser()
            temp_config_obj.read(temp_config)

            # Get paths using utils.get_paths
            config_path, audio_files_path = utils.get_paths(temp_config)

            # Add App section with required paths
            if "App" not in temp_config_obj:
                temp_config_obj["App"] = {}
            temp_config_obj["App"]["config_path"] = config_path
            temp_config_obj["App"]["audio_files_path"] = audio_files_path

            # Create args dictionary
            args = {
                "config": temp_config,
                "listvoices": False,
                "preview": False,
                "style": "",
                "styledegree": None,
            }

            # Store original state
            original_config = utils.config if hasattr(utils, 'config') else None
            original_config_path = utils.config_path if hasattr(utils, 'config_path') else None
            original_audio_path = utils.audio_files_path if hasattr(utils, 'audio_files_path') else None

            # Initialize utils with proper format
            utils.init(temp_config_obj, args)

            # Initialize tts_utils with utils
            tts_utils.init(utils)

            # Temporarily change audio files path to save to desired location
            original_audio_path = utils.audio_files_path
            utils.audio_files_path = os.path.dirname(filename)

            # Use tts_utils.speak to generate and save the audio
            tts_utils.speak(text, list_voices=False)

            # Find the generated audio file and rename it to desired filename
            import glob
            import time
            time.sleep(1)  # Wait for file to be written

            # Look for recently created audio files
            audio_files = glob.glob(os.path.join(utils.audio_files_path, "*.wav"))
            if audio_files:
                # Get the most recent file
                latest_file = max(audio_files, key=os.path.getctime)
                # Move it to desired location
                import shutil
                shutil.move(latest_file, filename)
            else:
                raise Exception("Audio file was not generated")

        finally:
            # Restore original settings
            if 'original_audio_path' in locals():
                utils.audio_files_path = original_audio_path
            self.config.set("TTS", "save_audio_file", original_save_setting)

            # Restore original state
            if original_config and original_config_path and original_audio_path:
                utils.config = original_config
                utils.config_path = original_config_path
                utils.audio_files_path = original_audio_path
                tts_utils.utils = utils

            # Clean up temp file
            if self.temp_config_path and os.path.exists(self.temp_config_path):
                try:
                    os.unlink(self.temp_config_path)
                    self.temp_config_path = None
                except:
                    pass
    
    def create_temp_config(self):
        """Create temporary configuration file for testing (no caching, no file saving)"""
        if self.temp_config_path:
            try:
                os.unlink(self.temp_config_path)
            except:
                pass

        # Create temporary file
        fd, self.temp_config_path = tempfile.mkstemp(suffix='.cfg', prefix='aac_gui_test_')
        os.close(fd)

        # Create a copy of config for testing with modifications
        temp_config = configparser.ConfigParser()
        temp_config.read_dict({section: dict(self.config[section]) for section in self.config.sections()})

        # Disable caching and file saving for testing
        if not temp_config.has_section("TTS"):
            temp_config.add_section("TTS")
        temp_config.set("TTS", "save_audio_file", "False")  # Don't save audio files during testing

        # Disable translation (not needed for TTS testing)
        if not temp_config.has_section("translate"):
            temp_config.add_section("translate")
        temp_config.set("translate", "no_translate", "True")  # Skip translation

        # Write modified configuration
        with open(self.temp_config_path, 'w') as f:
            temp_config.write(f)

        return self.temp_config_path

    def test_tts_playback(self, text):
        """Test TTS playback with current configuration using existing tts_utils"""
        # Create temporary config
        temp_config_path = self.create_temp_config()

        try:
            # Load the temporary config file
            temp_config = configparser.ConfigParser()
            temp_config.read(temp_config_path)

            # Get paths using utils.get_paths
            config_path, audio_files_path = utils.get_paths(temp_config_path)

            # Add App section with required paths
            if "App" not in temp_config:
                temp_config["App"] = {}
            temp_config["App"]["config_path"] = config_path
            temp_config["App"]["audio_files_path"] = audio_files_path

            # Create args dictionary
            args = {
                "config": temp_config_path,
                "listvoices": False,
                "preview": False,
                "style": "",
                "styledegree": None,
            }

            # Store original state
            original_config = utils.config if hasattr(utils, 'config') else None
            original_config_path = utils.config_path if hasattr(utils, 'config_path') else None
            original_audio_path = utils.audio_files_path if hasattr(utils, 'audio_files_path') else None

            # Initialize utils with proper format
            utils.init(temp_config, args)

            # Initialize tts_utils with utils
            tts_utils.init(utils)

            # Use tts_utils.speak to play the text (list_voices=False for playback)
            tts_utils.speak(text, list_voices=False)

        finally:
            # Restore original state
            if original_config and original_config_path and original_audio_path:
                utils.config = original_config
                utils.config_path = original_config_path
                utils.audio_files_path = original_audio_path
                tts_utils.utils = utils

            # Clean up temp file
            if self.temp_config_path and os.path.exists(self.temp_config_path):
                try:
                    os.unlink(self.temp_config_path)
                    self.temp_config_path = None
                except:
                    pass



    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_config_path and os.path.exists(self.temp_config_path):
            try:
                os.unlink(self.temp_config_path)
            except:
                pass


def main():
    """Main entry point"""
    app = QApplication(sys.argv)

    try:
        window = GUIConfigTester()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
