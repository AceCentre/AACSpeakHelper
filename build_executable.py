import subprocess
import os 

build_GUI = subprocess.run(["pyinstaller", ".\GUI\GUI_TranslateAndTTS\widget.spec"])
print("The exit code was: %d" % build_GUI.returncode)

build_translatepb = subprocess.run(["pyinstaller", "translatepb.spec"])
print("The exit code was: %d" % build_translatepb.returncode)
