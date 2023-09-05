python -m PyInstaller translatepb.py --noupx --noconsole --onedir -i .\assets\translate.ico --clean
python -m PyInstaller .\GUI_TranslateAndTTS\widget.py --noupx --noconsole --name "Configure TranslateAndTTS" --onefile  -i .\assets\configure.ico --clean
del *.spec
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\buildscript.iss