# AACSpeakHelper TTS Preview Tool

The TTS Preview Tool provides a user-friendly graphical interface for testing TTS engines and voices with AACSpeakHelper. This is a preview/testing tool that loads settings.cfg as defaults but does not save changes back to the configuration file.

## Features

### TTS Engine Selection
- Dropdown selection of available TTS engines (Azure TTS, Google TTS, Sherpa-ONNX, etc.)
- Uses the same TTS_ENGINES mapping as the CLI tool for consistency
- Automatically updates configuration when engine is changed

### Configuration Management
- Input fields for engine-specific credentials (API keys, regions, etc.)
- Follows the fixed configuration structure: stores voice_id ONLY in engine-specific sections
- Temporary configuration writer - does not permanently modify main settings.cfg
- Loads current configuration values as defaults when available
- Password masking for sensitive credential fields

### Voice Selection and Testing
- Voice selection dropdown populated based on chosen TTS engine
- Manual voice ID entry for engines without predefined voice lists
- Text input box for test phrases with default sample text
- "Play TTS" button to test audio output with current settings
- "Save as WAV" button to export audio file with automatic filename generation

## Usage

### Development Environment
```bash
# Run the GUI tool in development
uv run python gui_config_tester.py
```

### Installed Version
After installation, the TTS Preview Tool will be available as:
- **Executable**: `AACSpeakHelper TTS Preview.exe`
- **Start Menu**: "AACSpeakHelper TTS Preview"
- **Desktop Shortcut**: "AACSpeakHelper TTS Preview" (if desktop icons are enabled)
- **Post-Install Option**: "Launch TTS Preview Tool" after installation

## Interface Overview

### Engine Selection Section
- **Engine Dropdown**: Select from available TTS engines
- **Refresh Voices Button**: Update voice list for current engine

### Configuration Section
- **Credential Fields**: Dynamically generated based on selected engine
- **Voice Selection**: Dropdown or text input for voice ID

### Testing Section
- **Test Text Area**: Enter text to test with TTS (default provided)
- **Play TTS Button**: Test audio playback with current settings
- **Save as WAV Button**: Export audio to file

### Status Bar
- Shows current status and feedback messages

## Technical Implementation

### Framework
- Built with PySide6 (Qt6 for Python)
- Integrates with existing `tts_utils.py` and TTS engine initialization code
- Compatible with the fixed configuration system (voice_id in engine sections only)

### Configuration Handling
- Creates temporary configuration files for testing
- Does not modify the main settings.cfg file
- Follows the same engine naming conventions as CLI tool
- Respects the current pipe server architecture

### Error Handling
- Graceful handling of TTS engine errors with user-friendly messages
- Validation of configuration before testing
- Automatic cleanup of temporary files

### File Operations
- Automatic WAV filename generation from input text
- Sanitized filenames for filesystem compatibility
- File save dialog with proper file type filtering

## Integration with Build System

The GUI tool is integrated into the build system:

### PyInstaller Build
```bash
# Included in build_executable.bat
uv run python -m PyInstaller gui_config_tester.py --noupx --noconsole --name "Configure AACSpeakHelper GUI" --onedir --clean -i .\assets\configure.ico -y
```

### Inno Setup Installer
- Included in the Windows installer
- Available as a post-install launch option
- Desktop shortcut creation available

## Dependencies

### Required Packages
- PySide6 (already included in project dependencies)
- All existing AACSpeakHelper dependencies
- No additional external dependencies required

### Module Dependencies
- `cli_config_creator.py` - For TTS_ENGINES mapping and configuration utilities
- `tts_utils.py` - For TTS engine initialization and audio processing
- `utils.py` - For configuration management and audio file handling

## Compatibility

### Environment Support
- Works in both development (uv run) and installed executable environments
- Compatible with existing CLI config creator without conflicts
- Follows the same configuration structure and engine naming conventions

### Configuration System
- Respects the fixed configuration system established in recent updates
- Stores voice_id only in engine-specific sections, not in [TTS] section
- Compatible with all supported TTS engines

## Troubleshooting

### Common Issues

**GUI doesn't start**
- Ensure PySide6 is installed: `uv add PySide6`
- Check that all required modules are available

**TTS test fails**
- Verify engine credentials are configured correctly
- Ensure voice_id is selected for the current engine
- Check that the TTS engine is properly installed

**Audio file save fails**
- Verify write permissions to target directory
- Ensure sufficient disk space
- Check that the TTS engine supports audio file generation

### Debug Information
- Status bar shows current operation status
- Error dialogs provide detailed error messages
- Temporary configuration files are automatically cleaned up

## Future Enhancements

Potential improvements for future versions:
- Voice preview functionality
- Batch testing with multiple engines
- Configuration export/import
- Advanced audio settings (rate, volume, pitch)
- Real-time voice list fetching from TTS APIs
