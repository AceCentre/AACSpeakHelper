# Tips

#### Can I use this to batch-process a file of strings?

Sure. You may want to do this, for example, to create audio files for some phrases for a bilingual speaker. There are other tools to do this, but this is possible. You can just copy your text and run the main application - then look at the cache directory for the audio file. But if you want to automate this, check out this Powershell script

```
# Define the path to the text file and executable
$textFilePath = "C:\path\to\textfile.txt"
$executablePath = "C:\Program Files (x86)\Ace Centre\TranslateAndTTS\translatepb.exe"
$outputFolder = "C:\path\to\output\folder"

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

        # Wait for the executable to complete and the file to be created (adjust time as needed)
        Start-Sleep -Seconds 5

        # Identify the latest created file in the output folder (assuming it's sorted by date)
        $latestFile = Get-ChildItem $outputFolder | Sort-Object LastWriteTime -Descending | Select-Object -First 1

        # Generate a unique truncated name based on the line from textFilePath
        $truncatedName = $line.Substring(0, [Math]::Min(10, $line.Length)) # Taking first 10 characters, adjust as needed

        # Rename the file
        Rename-Item -Path "$outputFolder\$($latestFile.Name)" -NewName "$truncatedName.txt" # Adjust extension if needed
    }
} else {
    Write-Host "Text file not found at $textFilePath"
}

```

#### When supporting people with a language not supported by AAC

* Does the Voice exist on any system? (See our[ links here](supported-languages.md))
* If it doesnt can we get by with recorded clips?
* Do we need symbol vocabulary or can they write?
* If they can write what script are they familar with (Hint: Ask them if they write in their language to their friends on their phone - if they use the standard latin (UK/US) keyboard  they _could be using transliteration._ This is not bad - you will just have to test if your TTS engine works with that. And remember if you are going to do phrases you may want to use transliteration too if they are not familar with the written form )
*

