###
# python your_script.py "C:\Users\Local\Roaming.."
# 
# UpdateFilePathGridset.exe "C:\Users\Local\Roaming.."
#
###

import zipfile
import os
import re
import argparse

def modify_gridset(gridset_path, LocalAppPath):
	temp_dir = 'temp_gridset'
	os.makedirs(temp_dir, exist_ok=True)
	
	with zipfile.ZipFile(gridset_path, 'r') as zip_ref:
		zip_ref.extractall(temp_dir)
	
	for foldername, _, filenames in os.walk(temp_dir):
		for filename in filenames:
			if filename.endswith('.xml'):
				xml_path = os.path.join(foldername, filename)
				
				with open(xml_path, 'r') as f:
					filedata = f.read()
				
				new_data = re.sub('%FILEPATHTOREPLACE%', LocalAppPath, filedata)
				
				with open(xml_path, 'w') as f:
					f.write(new_data)
	
	new_gridset_path = os.path.join(os.path.expanduser("~"), 'Desktop', 'Example Pages', 'modified_gridset.gridset')
	os.makedirs(os.path.dirname(new_gridset_path), exist_ok=True)
	with zipfile.ZipFile(new_gridset_path, 'w') as zipf:
		for root, _, files in os.walk(temp_dir):
			for file in files:
				zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Update File Path in Gridset')
	parser.add_argument('LocalAppPath', type=str, help='The path to replace %FILEPATHTOREPLACE% in .xml files')
	args = parser.parse_args()

	local_app_data_path = os.environ.get('LOCALAPPDATA', 'TranslateAndTTS')
	# Assuming the original gridset is located at 'original_gridset.gridset'
	modify_gridset(local_app_data_path+'TranslateAndTTS DemoGridset.gridset', args.LocalAppPath)
