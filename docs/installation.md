# Installation

#### Step 1: Download

Download the installer from [our latest release](https://github.com/AceCentre/TranslateAndTTS/releases/latest).

#### Step 2: Install

Run the installer. It will place the program in `C:\Program Files (x86)\Ace Centre\TranslateAndTTS\translatepb.exe`. All settings, cache data, etc., are in `%AppData%\TranslateAndTTS`

#### Step 3: Configure

After installation, you need to configure the application. If you don't, it will default to using a free speech service provided by voices at translate.google.com and translation by mymemory. You can edit the settings file by hand or use our GUI application `Configure TranslateAndTTS`, which you can find in your start menu and Desktop.

![Screenshot of Configure App](https://raw.githubusercontent.com/AceCentre/TranslateAndTTS/main/assets/ConfigureTranslateAndTTSScreenshot.png)

**Notes on the configuration options**

**Text-to-Speech (TTS) Engine Selection**

* **Offline Support**: Only the SAPI engine operates entirely offline.
* **API Keys**: For Azure and Google TTS, you'll need to obtain API keys. Learn how to get them.
* **gTTS**: This is a free but limited option. The voice and language are determined by your **target lang** in translate. The way this works is it uses the voice found in the [Google Translate](https://translate.google.com) tool online. We don't use the translation service - just the voice. So not all languages are supported.
* **Kurdish TTS**: This engine has specific requirements. See details.

**Data Collection**

* **Minimal Tracking**: We collect basic usage statistics but do not personally identify users.
* **Transparency**: To see the exact data we collect, [view our code here](https://github.com/AceCentre/TranslateAndTTS/blob/05e1f68e287ef5a653aaeb2e21d2e89f4f7a3d85/utils.py#L271).

**Translation Services**

* **Setting Languages**: The most crucial step is to set both the **Writing** and **Target** languages.
* **Free Tier**: The default free service is [myMemory](http://mymemory.translated.net). If you find it lacking for your language pair, you can switch to a paid service.
* **Paid Tier**: [DeepL](https://www.deepl.com/translator) offers comprehensive language coverage and is highly recommended. But you may want to try the others.
* **AAC Software Integration**: To make the translated string available in your AAC software, check the box to overwrite the clipboard.

You can edit the settings file by hand if you wish. To do this, navigate to `%AppData%\TranslateAndTTS` in File Explorer to find the `settings.cfg` file. Edit the configuration using either a plain text editor.

**Note: You can copy this settings file and have numerous versions of them - or make it and distribute it to an end user. You would use the `--config file path to run the application using a different config file.cfg` parameter**

#### Step 4. Add your support to your AAC software.

See below for specific details, but in short;

* Add a button to _copy_ the message bar (writing area)
* Then have an action on this button to call the executable found at `C:\Program Files (x86)\Ace Centre\TranslateAndTTS\translatepb.exe`
* Then it's wise to wait around 5-10 seconds (and if translating text)
* Clear the message bar
* Paste the returning text back if you are translating

You can test it by copying some text from a text file and running the app. Give it a go.
