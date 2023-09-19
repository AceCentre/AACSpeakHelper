# Tips

#### Can I use this to batch-process a file of strings?

Sure. You may want to do this, for example, to create audio files for some phrases for a bilingual speaker. There are other tools to do this, but this is possible. You can just copy your text and run the main application - then look at the cache directory for the audio file. But if you want to automate this, check out this Powershell script

```
# Define the path to the text file and executable
$textFilePath = "C:\path\to\textfile.txt"
$executablePath = "C:\Program Files (x86)\Ace Centre\TranslateAndTTS\translatepb.exe"

# Check if text file exists
if (Test-Path $textFilePath) {
	# Read each line of the text file
	$lines = Get-Content $textFilePath

	# Iterate through each line
	foreach ($line in $lines) {
		# Copy the line to the clipboard
		$line | Set-Clipboard
	
		# Run the executable
		Start-Process $executablePath
	
		# Wait a bit before processing the next line (optional)
		Start-Sleep -Seconds 2
	}
} else {
	Write-Host "Text file not found at $textFilePath"
}
```

#### Using RHVoice for minority languages offline

[RHVoice](https://rhvoice.org) is a great project creating TTS Systems for minority languages. Its also great because they work offline. This isnt so much of a tip but a reminder that the project exists. To install SAPI voices for this system see the [prebuilt binaries here](https://github.com/RHVoice/RHVoice/blob/master/doc/en/Binaries.md). RHVoice supports:

* American and Scottish English
* Brazilian Portuguese
* Esperanto
* Georgian
* Ukrainian
* Kyrgyz
* Tatar
* Macedonian
* Albanian
* Polish
