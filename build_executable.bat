@echo off

REM Get site-packages path
for /f "tokens=*" %%i in ('uv run python -c "import site; print(site.getsitepackages()[0])"') do set site_packages=%%i\Lib\site-packages

REM Echo the site-packages path for debugging
echo Site packages path: %site_packages%

REM Convert UI files using Python module
uv run python -m PySide6.uic.pyuic GUI_TranslateAndTTS/form.ui -o GUI_TranslateAndTTS/ui_form.py
uv run python -m PySide6.uic.pyuic GUI_TranslateAndTTS/item.ui -o GUI_TranslateAndTTS/item.py

REM Build Python executables with PyInstaller
uv run python -m PyInstaller AACSpeakHelperServer.py --noupx --onedir --noconsole --name "AACSpeakHelperServer" -i .\assets\translate.ico --clean --collect-binaries azure.cognitiveservices.speech --add-binary "C:\Windows\System32\winmm.dll;." --add-binary "C:\Windows\System32\dsound.dll;." --add-binary "C:\Windows\System32\AudioEng.dll;." --add-binary "C:\Windows\System32\AudioSes.dll;." --add-binary "C:\Windows\System32\AUDIOKSE.dll;." --add-binary "C:\Windows\System32\mf.dll;." --add-binary "C:\Windows\System32\mfplat.dll;." --add-binary "C:\Windows\System32\MMDevAPI.dll;." --collect-all language_data --collect-all language_tags --collect-all comtypes --collect-all pytz --collect-all sounddevice --collect-all pyaudio -y

uv run python -m PyInstaller .\GUI_TranslateAndTTS\widget.py --noupx --noconsole --name "Configure AACSpeakHelper" --onedir -i .\assets\configure.ico --clean --collect-binaries azure.cognitiveservices.speech --collect-all language_data --collect-all language_tags --collect-all pytz --collect-all comtypes -y

uv run python -m PyInstaller client.py --noupx --console --onedir --clean -i .\assets\translate.ico -y

uv run python -m PyInstaller cli_config_creator.py --noupx --console --name "Configure AACSpeakHelper CLI" --onedir --clean -i .\assets\configure.ico -y

uv run python -m PyInstaller CreateGridset.py --noupx --noconsole --onedir --clean -y

REM Run Inno Setup (if available)
if exist "C:\Users\admin.will\AppData\Local\Programs\Inno Setup 6\ISCC.exe" (
    echo Running Inno Setup to create installer...
    "C:\Users\admin.will\AppData\Local\Programs\Inno Setup 6\ISCC.exe" buildscript.iss
) else if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo Running Inno Setup to create installer...
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" buildscript.iss
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    echo Running Inno Setup to create installer...
    "C:\Program Files\Inno Setup 6\ISCC.exe" buildscript.iss
) else (
    echo Inno Setup not found. Skipping installer creation.
    echo To create an installer, please install Inno Setup from: https://jrsoftware.org/isdl.php
    echo Then re-run this build script.
)