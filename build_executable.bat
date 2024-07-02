python -m PyInstaller translatepb.py --noupx --noconsole --onedir -i .\assets\translate.ico --clean
python -m PyInstaller .\GUI_TranslateAndTTS\widget.py --noupx --noconsole --name "Configure AACSpeechHelper" --onefile  -i .\assets\configure.ico --clean
del *.spec
python -m PyInstaller CreateGridset.py --noupx --noconsole --onedir --clean
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\buildscript.iss