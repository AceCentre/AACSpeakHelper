@echo off

REM Get site-packages path
for /f "tokens=*" %%i in ('uv run python -c "import site; print(site.getsitepackages()[0])"') do set site_packages=%%i

REM Echo the site-packages path for debugging
echo Site packages path: %site_packages%

REM Convert UI files
uv run python -m PySide6.uic.pyuic GUI_TranslateAndTTS/form.ui -o GUI_TranslateAndTTS/ui_form.py
uv run python -m PySide6.uic.pyuic GUI_TranslateAndTTS/item.ui -o GUI_TranslateAndTTS/item.py

REM Build Python executables with PyInstaller
uv run python -m PyInstaller AACSpeakHelperServer.py --noupx --onedir --noconsole --name "AACSpeakHelperServer" -i .\assets\translate.ico --clean --add-binary "%site_packages%\azure\cognitiveservices\speech\Microsoft.CognitiveServices.Speech.core.dll;." --collect-all language_data --collect-all language_tags --collect-all comtypes --collect-all pytz -y

uv run python -m PyInstaller .\GUI_TranslateAndTTS\widget.py --noupx --noconsole --name "Configure AACSpeakHelper" --onedir -i .\assets\configure.ico --clean --add-binary "%site_packages%\azure\cognitiveservices\speech\Microsoft.CognitiveServices.Speech.core.dll;." --collect-all language_data --collect-all language_tags --collect-all pytz --collect-all comtypes -y

uv run python -m PyInstaller client.py --noupx --noconsole --onedir --clean -i .\assets\translate.ico -y

uv run python -m PyInstaller CreateGridset.py --noupx --noconsole --onedir --clean -y

REM Run Inno Setup
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" buildscript.iss