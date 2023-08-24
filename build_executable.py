import subprocess

build_GUI = subprocess.run(["pyinstaller", ".\GUI_TranslateAndTTS\widget.spec"])
print("The exit code was: %d" % build_GUI.returncode)

build_translatepb = subprocess.run(["pyinstaller", "translatepb.spec"])
print("The exit code was: %d" % build_translatepb.returncode)
