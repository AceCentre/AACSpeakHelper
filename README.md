<img src='https://raw.githubusercontent.com/AceCentre/TranslateAndTTS/main/assets/translatepb.png' alt="Blue logo with translate icon" width="200">

# AAC Online Speak & Translate Plug-in for Windows ("AAC Speak Helper")

Copies the pasteboard. Translates to defined lang, Reads aloud and replaces pasteboard with translated text. You can can configure it all with our Configure app - and use multiple different settings files for different actions. Using Google or Azure Cloud TTS we have a greater range of languages and voices than any current AAC solution. 

## Who needs this

Imagine the scenario. You rely on technology to communicate, but you only speak in Ukranian and have little expressive skills in English. You are in a care setting. We need a quick translation tool using your existing technology to translate from your known language to English so you can communicate with your carers. This does that. 

It also allows people who natively need to speak in less well supported languages  a way of using text to speech. 

<div>
    <a href="https://www.loom.com/share/dcd185df50224279a0c2630b6ca6b04f">
      <p>Overview of our AAC Helper Tool for Translation and Speaking in different languages - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/dcd185df50224279a0c2630b6ca6b04f">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/dcd185df50224279a0c2630b6ca6b04f-1694639990490-with-play.gif">
    </a>
  </div>
  
## What does it work with?

It's a small windows executable. You call it from your Windows AAC app if it has a way of running external programs. Most Windows AAC apps can. 

## How does it work?

So as long as some text is in the copy buffer (e.g. ctrl+c) - it will then read that text. Depending on the settings file it will then either translate that text using the preferred service and then speak it out loud - or just speak out loud the passed string. 

## Where do I download it?

We have an installer - which you can find [here](https://github.com/AceCentre/TranslateAndTTS/releases/latest). Our instructions and demo pages for devices are using the installer. 

## How do I install it?

Run the installer. It will put the program in `C:\Program Files (x86)\Ace Centre\TranslateAndTTS\`

Next, you will need to edit the *settings.cfg* file. Find this at  `%AppData%\TranslateAndTTS` (NB: Put this path into the file explorer) - However its easiest setting this up with the `Configure TranslateAndTTS` app which is found in your Start Menu (and Desktop if you checked the box at install)

You can also edit do this in a plain text editor such as Notepad. It Looks like this:

	[App]
	uuid = ce79bca5-691d-4cb2-8a8c-6fb7b74d4ce6
	# We collect anonymous aggregrate stats. Like how many times it was installed. To turn this off set to false
	collectstats = True

	[translate]
	# Want to JUST speak  - set this to true
	notranslate = False
	# What language do you write in?
	startlang = en
	# What language do you translate to?
	endlang = es
	# If you do not want to overwrite the pasteboard with the translated text set to False
	replacepb = True
	# MyMemoryProvider is free - but if you want to increase the amount of translations place here a key for one of the services
	# Set provider to the name of the service
	provider = MyMemoryProvider
	mymemoryprovider_secret_key = 
	email = 
	libreprovider_secret_key = 
	url = 
	deeplprovider_secret_key = 
	deepl_pro = false
	microsoftprovider_secret_key = 
	region = 

	[TTS]
	# We can use quite a wide array of Text to Speech engines 
	# Engine = azureTTS, googleTTS, kurdishTTS, sapi5 (windows), coqui_ai_tts nsss (mac), espeak, gTTS (Free - voice that comes from Google Translate), Google cloud and Azure both need API keys
	engine = gTTS
	save_audio_file = True
	voiceid = 
	rate = 100
	volume = 100

	[azureTTS]
	key = 
	location = 
	voiceid = en-US-JennyNeural

	[googleTTS]
	creds_file = //mac/Home/Downloads/ttsandtranslate-d51533198395.json
	voiceid = en-US-Wavenet-C

	[sapi5TTS]
	voiceid = HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0

	[kurdishTTS]
	latin = true
	punctuation = false


Edit any of the items here - the essential one is what is your Start Language (What do you write in) - and what is your End Language? (What you want it translated to). See below for what Language codes are available. Note the TTS options. You can use SAPI - just make sure the VoiceID is listed. You can find this out by running the app with a flag of `--listvoices` in the command line. gTTS is using Google's TTS system. At this time you can't choose your voice - it will just pick the first one that matches the language code. We might change this at some point. 

*Note* - if you just want to use this tool to act as a bridge to the other TTS systems - mark noTranslate as True - and it will just read out the messaagebar text

Next, in your AAC software, you need to create a button. This button needs to 

1. Copy the message bar.
2. Call the application found in the folder you created earlier e.g `C:\translatepb\translatepb.exe`
3. Wait (e.g. 5-10 secs)
4. Paste (this pastes the translated text back into the message bar). You can look at this example gridset for some help 

## How do I get keys for Azure or Google Cloud TTS?

### Languages supported

These are the languages supported by Azure

- Afrikaans
 - Amharic
 - Arabic
 - Azerbaijani
 - Bulgarian
 - Bangla
 - Bengali
 - Bosnian
 - Catalan
 - Czech
 - Welsh
 - Danish
 - German
 - Greek
 - English
 - Spanish
 - Estonian
 - Persian
 - Finnish
 - Filipino
 - French
 - Irish
 - Galician
 - Gujarati
 - Hebrew
 - Hindi
 - Croatian
 - Hungarian
 - Armenian
 - Indonesian
 - Icelandic
 - Italian
 - Japanese
 - Javanese
 - Georgian
 - Kazakh
 - Khmer
 - Kannada
 - Korean
 - Lao
 - Lithuanian
 - Latvian
 - Macedonian
 - Malayalam
 - Mongolian
 - Marathi
 - Malay
 - Maltese
 - Burmese
 - Norwegian Bokmål
 - Nepali
 - Dutch
 - Polish
 - Pashto
 - Portuguese
 - Romanian
 - Russian
 - Sinhala
 - Slovak
 - Slovenian
 - Somali
 - Albanian
 - Serbian
 - Sundanese
 - Swedish
 - Swahili
 - Tamil
 - Telugu
 - Thai
 - Turkish
 - Ukrainian
 - Urdu
 - Uzbek
 - Vietnamese
 - Chinese

These are the languages supported by Google Cloud

 - Afrikaans (South Africa)
 - Arabic
 - Basque (Spain)
 - Bengali (India)
 - Bulgarian (Bulgaria)
 - Catalan (Spain)
 - Chinese (Hong Kong)
 - Czech (Czech Republic)
 - Danish (Denmark)
 - Dutch (Belgium)
 - Dutch (Netherlands)
 - English (Australia)
 - English (India)
 - English (UK)
 - English (US)
 - Filipino (Philippines)
 - Finnish (Finland)
 - French (Canada)
 - French (France)
 - Galician (Spain)
 - German (Germany)
 - Greek (Greece)
 - Gujarati (India)
 - Hebrew (Israel)
 - Hindi (India)
 - Hungarian (Hungary)
 - Icelandic (Iceland)
 - Indonesian (Indonesia)
 - Italian (Italy)
 - Japanese (Japan)
 - Kannada (India)
 - Korean (South Korea)
 - Latvian (Latvia)
 - Lithuanian (Lithuania)
 - Malay (Malaysia)
 - Malayalam (India)
 - Mandarin Chinese
 - Marathi (India)

### Azure TTS

- You first need Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services).
- [Create a Speech resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices) in the Azure portal.
- Your Speech resource key and region. After your Speech resource is deployed, select Go to resource to view and manage keys. For more information about Azure AI services resources, see [Get the keys for your resource](https://learn.microsoft.com/en-us/azure/ai-services/multi-service-resource?pivots=azportal#get-the-keys-for-your-resource)

Note: You can use the ``--style`` flag on the command line for Azure voices. If you do this follow it by one of these style flags. 

- advertisement_upbeat
- affectionate
- angry
- assistant
- calm
- chat
- cheerful
- customerservice
- depressed
- disgruntled
- documentary-narration
- embarrassed
- empathetic
- envious
- excited
- fearful
- friendly
- gentle
- hopeful
- lyrical
- narration-professional
- narration-relaxed
- newscast
- newscast-casual
- newscast-formal
- poetry-reading
- sad
- serious
- shouting
- sports_commentary
- sports_commentary_excited
- whispering
- terrified
- unfriendly


### Google Cloud TTS

Creating a service account for OAuth 2.0 involves generating credentials for a non-human user, often used in server-to-server interactions. Here's how you can create OAuth 2.0 credentials using a service account for Google APIs:

Go to the Google Cloud Console:
Visit the Google Cloud Console.

Create a New Project:
If you don't have a project already, create a new project in the developer console.

Enable APIs:
Enable the APIs that your service account will be using. For example, if you're using Google Drive API, enable that API for your project.

Create a Service Account:

1. Go to the Google Cloud Console:
Visit the [Google Cloud Console](https://console.cloud.google.com/).

2. Create a New Project:
If you don't have a project already, create a new project in the developer console.

3. Enable APIs:
Enable the APIs that your service account will be using. For example, if you're using Google Drive API, enable that API for your project.

4. Create a Service Account:
- In the Google Cloud Console, navigate to "IAM & Admin" > "Service accounts."
- Click on "Create Service Account."
- Enter a name for the service account and an optional description.
- Choose the role for the service account. This determines the permissions it will have.
- Click "Continue" to proceed.

5. Create and Download Credentials:
- On the next screen, you can choose to grant the service account a role on your project. You can also skip this step and grant roles later.
- Click "Create Key" to create and download the JSON key file. This file contains the credentials for your service account.
- Keep this JSON file secure and do not expose it publicly.

6. Use the Service Account Credentials:
- In your code, load the credentials from the JSON key file. The credentials can be used to authenticate and access the APIs on behalf of the service account.

7. Grant Required Permissions:
- If you skipped assigning roles during the service account creation, you can now grant roles to the service account by navigating to "IAM & Admin" > "IAM" and adding the service account's email address with the appropriate roles.

## What if I have a problem?

Right now, this is a very, very quick (and dirty) example. We dare say there will be *SIGNIFICANT* problems using this. Remember if you use the gTTS option, it must be online. Translating too. We have put no logic in the script to deal with this failure. 

If you wish to improve the code and have the skills to, please fork and PR. Or consider [donating](https://acecentre.org.uk/get-involved/donate) to us and asking for specific support for this.
 
## AAC Specific Guides

### Snap

![Screenshot of how to call a program](assets/AAC-Screen-Snap.jpg)

### The Grid 3

See the demo gridset [here](https://github.com/AceCentre/TranslateAndTTS/tree/main/assets)

### Communicator

See the demo pageset [here](https://github.com/AceCentre/TranslateAndTTS/tree/main/assets)

![Screenshot of how to call a program](assets/AAC-Screen-Communicator.png)



### NuVoice

### MindExpress

Don't bother - MEX already can do this. See [here for a demo](https://www.jabbla.co.uk/vocab/translation-tool/)

## Developer details

- See build details [here](https://github.com/AceCentre/TranslateAndTTS/blob/main/.github/workflows/windows-build-release.yml)
- 
