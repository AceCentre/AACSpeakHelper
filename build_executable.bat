python -m PyInstaller translatepb.py --noupx --onedir --noconsole -i .\assets\translate.ico --clean --add-binary "venv/Lib/site-packages/azure/cognitiveservices/speech/Microsoft.CognitiveServices.Speech.core.dll;." --add-data "venv/Lib/site-packages/ttsmms/commons.py;." --collect-all language_data --collect-all language_tags --collect-all comtypes --collect-all pytz -y
python -m PyInstaller .\GUI_TranslateAndTTS\widget.py --noupx --noconsole --name "Configure AACSpeechHelper" --onedir -i .\assets\configure.ico --clean --add-binary "venv/Lib/site-packages/azure/cognitiveservices/speech/Microsoft.CognitiveServices.Speech.core.dll;." --add-data "venv/Lib/site-packages/ttsmms/commons.py;." --collect-all language_data --collect-all language_tags --collect-all pytz --collect-all comtypes -y
python -m PyInstaller CreateGridset.py --noupx --noconsole --onedir --clean -y
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\buildscript.iss