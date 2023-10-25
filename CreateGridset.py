import zipfile
import os
import re
import shutil  # Import the shutil module

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
				
				new_data = re.sub('%FILEPATHTOREPLACE%', re.escape(LocalAppPath), filedata)
				
				with open(xml_path, 'w') as f:
					f.write(new_data)
	
	new_gridset_path = os.path.join(os.path.expanduser("~"), 'Desktop', 'Example AAC Helper tool Pages', 'modified_gridset.gridset')
	os.makedirs(os.path.dirname(new_gridset_path), exist_ok=True)
	with zipfile.ZipFile(new_gridset_path, 'w') as zipf:
		for root, _, files in os.walk(temp_dir):
			for file in files:
				zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))
	
	# Delete the temp directory after creating the modified .gridset
	shutil.rmtree(temp_dir)
	os.remove(gridset_location)


if __name__ == "__main__":
	app_data_path = os.environ.get('APPDATA', '')  # Changed to APPDATA
	gridset_location = os.path.join(app_data_path, 'TranslateAndTTS', 'TranslateAndTTS DemoGridset.gridset')  # Updated path
	
	# Assuming the original gridset is located at 'TranslateAndTTS DemoGridset.gridset' within the APPDATA folder
	modify_gridset(gridset_location, app_data_path)
