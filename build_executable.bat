@echo off
setlocal

rem Capture the Poetry environment path
for /f "delims=" %%i in ('poetry env info --path') do set venv_path=%%i

rem Construct the site-packages path
set site_packages=%venv_path%\Lib\site-packages

rem Echo the constructed site-packages path for debugging
echo Site packages path: %site_packages%

rem Build Python executables with PyInstaller
poetry run python -m PyInstaller AACSpeakHelperServer.py --noupx --onedir --noconsole --name "AACSpeakHelperServer" -i .\assets\translate.ico --clean --add-binary "%site_packages%\azure\cognitiveservices\speech\Microsoft.CognitiveServices.Speech.core.dll;." --collect-all language_data --collect-all language_tags --collect-all comtypes --collect-all pytz -y
poetry run python -m PyInstaller .\GUI_TranslateAndTTS\widget.py --noupx --noconsole --name "Configure AACSpeakHelper" --onedir -i .\assets\configure.ico --clean --add-binary "%site_packages%\azure\cognitiveservices\speech\Microsoft.CognitiveServices.Speech.core.dll;." --collect-all language_data --collect-all language_tags --collect-all pytz --collect-all comtypes -y
poetry run python -m PyInstaller client.py --noupx --noconsole --onedir --clean -i .\assets\translate.ico -y
poetry run python -m PyInstaller CreateGridset.py --noupx --noconsole --onedir --clean -y

"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\buildscript.iss

endlocal