# AACSpeakHelper Audio Troubleshooting Guide

## The Issue
You're seeing this error in the logs:
```
OSError: [Errno -9985] Device unavailable
```

This means the audio output device is not accessible to the AACSpeakHelper application.

## Quick Fixes to Try

### 1. **Check if Audio Device is in Use**
- Close any other applications that might be using audio (media players, video calls, etc.)
- Try playing audio from another application to confirm your speakers/headphones work
- Restart AACSpeakHelper after closing other audio applications

### 2. **Restart Windows Audio Service**
1. Press `Win + R`, type `services.msc`, press Enter
2. Find "Windows Audio" in the list
3. Right-click → Restart
4. Try AACSpeakHelper again

### 3. **Run as Administrator**
1. Right-click on AACSpeakHelper
2. Select "Run as administrator"
3. This can resolve permission issues with audio device access

### 4. **Check Audio Device Settings**
1. Right-click the speaker icon in system tray
2. Select "Open Sound settings"
3. Make sure your output device is set correctly
4. Test the device by clicking "Test" button

## Diagnostic Script

Run the `diagnose_installed_audio.py` script in your AACSpeakHelper installation directory. This will:
- Check if all required audio DLLs are present
- Test the server's audio functionality
- Examine log files for specific errors

## Advanced Troubleshooting

### If the diagnostic shows missing DLLs:
Your installation might be from an older build. Please:
1. Download the latest version of AACSpeakHelper
2. Uninstall the old version completely
3. Install the new version

### If DLLs are present but audio still fails:
This indicates a system-level audio issue:

1. **Update Audio Drivers**
   - Go to Device Manager
   - Expand "Sound, video and game controllers"
   - Right-click your audio device → Update driver

2. **Check Windows Audio Troubleshooter**
   - Go to Settings → Update & Security → Troubleshoot
   - Run "Playing Audio" troubleshooter

3. **Try Different Audio Output**
   - If you have multiple audio devices (speakers, headphones, etc.)
   - Try switching to a different one in Windows Sound settings

4. **Disable Audio Enhancements**
   - Right-click speaker icon → Open Sound settings
   - Click "Device properties" for your output device
   - Go to "Additional device properties"
   - In "Enhancements" tab, check "Disable all enhancements"

## Technical Details

The error occurs because:
1. AACSpeakHelper uses the `py3-tts-wrapper` library for text-to-speech
2. This library uses `sounddevice` for audio playback
3. `sounddevice` requires access to the PortAudio library
4. If PortAudio can't access the audio device, you get the "Device unavailable" error

## What We Fixed

Recent versions of AACSpeakHelper include fixes for:
- Missing PortAudio DLLs in the installation
- Proper inclusion of sounddevice audio dependencies
- Better PyInstaller packaging for audio libraries

## Still Having Issues?

If none of these steps work:

1. **Check the exact error time** in the log file
2. **Note what you were doing** when the error occurred
3. **Try the diagnostic script** and share the results
4. **Check if other audio applications work** at the same time

The issue is likely related to:
- Windows audio service conflicts
- Audio driver issues
- Multiple applications competing for audio access
- System permissions for audio device access

## Contact Support

If you continue to have issues, please provide:
1. The output from `diagnose_installed_audio.py`
2. The full error message from the log file
3. Your Windows version and audio hardware details
4. Whether other audio applications work normally
