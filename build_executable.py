import subprocess
import os 
def Test1(rootDir): 
    list_dirs = os.walk(rootDir) 
    for root, dirs, files in list_dirs: 
        for d in dirs: 
            print os.path.join(root, d)      
        for f in files: 
            print os.path.join(root, f) 
          
Test1('.')

build_GUI = subprocess.run(["pyinstaller", ".\GUI\GUI_TranslateAndTTS\widget.spec"])
print("The exit code was: %d" % build_GUI.returncode)

build_translatepb = subprocess.run(["pyinstaller", "translatepb.spec"])
print("The exit code was: %d" % build_translatepb.returncode)
