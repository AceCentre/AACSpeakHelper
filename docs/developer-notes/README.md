# Developer Notes

* It works on Python 3.10 or 3.11. The dependencies aren't well covered on all other versions (and there are a lot!)
* We use a GitHub action to build the application (see workflow [here](../../.github/workflows/windows-build-release.yml).)&#x20;

## Building the Application

### Development Testing
```powershell
# Test the server
uv run python AACSpeakHelperServer.py

# Test the client (in another terminal)
uv run python client.py

# Test CLI configuration tool
uv run python cli_config_creator.py
```

### Building for Windows
```powershell
# Use the automated build script
.\build_executable.bat

# Or build manually:
# Build server
uv run python -m PyInstaller AACSpeakHelperServer.py --noupx --onedir --noconsole --name "AACSpeakHelperServer" -i .\assets\translate.ico --clean

# Build client
uv run python -m PyInstaller client.py --noupx --console --onedir --clean -i .\assets\translate.ico

# Build CLI configuration tool
uv run python -m PyInstaller cli_config_creator.py --noupx --console --name "Configure AACSpeakHelper CLI" --onedir --clean -i .\assets\configure.ico

# Note: GUI configuration tool is excluded from builds due to reliability issues

# Build installer (requires Inno Setup 6)
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\buildscript.iss
```

