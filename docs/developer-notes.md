# Developer Notes

* It works on Python 3.10 or 3.11. The dependencies aren't well covered on all other versions (and there are a lot!)
* We use a GitHub action to build the application (see workflow [here](../.github/workflows/windows-build-release.yml).)&#x20;

```powershell
// Test
python translatepb.py
// Build for Windows
python -m PyInstaller translatepb.py --noupx --noconsole --onedir -i .\assets\translate.ico --clean
python -m PyInstaller .\GUI_TranslateAndTTS\widget.py --noupx --noconsole --name "Configure TranslateAndTTS" --onefile  -i .\assets\configure.ico --clean
// Build installer. 
//    You need to install InnoSetup (6) https://jrsoftware.org/isinfo.php
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" .\buildscript.iss
```

