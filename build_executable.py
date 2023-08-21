import subprocess
import os

application_path = os.path.dirname(__file__)
GUI_script_path = os.path.join(
    application_path, 'GUI', 'GUI_TranslateAndTTS', 'widget.spec')
translatepb_path = os.path.join(application_path,  'translatepb.spec')
print(GUI_script_path)
print(translatepb_path)
process = subprocess.run(["pyinstaller", GUI_script_path])
process2 = subprocess.run(["pyinstaller", translatepb_path])
