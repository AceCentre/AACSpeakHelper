# Installation

#### Step 1: Download

Download the installer from our [latest release.](https://github.com/AceCentre/AACSpeakHelper/releases/tag/vv2.2.1)

#### Step 2: Install

Run the installer. It will place the program in your local App Directory. This can be found by going to [`%UserProfile%\AppData\Local\Programs\Ace Centre\TranslateAndTTS\`](file:///%UserProfile%/AppData/Local/Programs/TranslateAndTTS) your File Explorer (or right-clicking on the desktop shortcut and selecting "**Open File Location**". All settings, cache data, etc., are in `%AppData%\TranslateAndTTS`

{% hint style="info" %}
Keep a note of the location of the Program Installation Directory. You need this for the AAC software integration
{% endhint %}

#### Step 3: Configure

After installation, you need to configure the application. If you don't, it will default to using a free speech service provided by voices at translate.google.com and translation by mymemory. You can edit the settings file by hand or use our GUI application `Configure TranslateAndTTS`, which you can find in your start menu and Desktop.

\\

<figure><img src=".gitbook/assets/Screenshot 2023-10-20 at 17.26.52.png" alt=""><figcaption><p>Choose a TTS Provider and voice</p></figcaption></figure>

<figure><img src=".gitbook/assets/Screenshot 2023-10-20 at 17.26.59 (2).png" alt=""><figcaption><p>Choose a translation provider</p></figcaption></figure>

<figure><img src=".gitbook/assets/App Settings.png" alt=""><figcaption><p>App Settings. Note Copy Path of Main app to add to your AAC software</p></figcaption></figure>

**Notes on the configuration options**

**Text-to-Speech (TTS) Engine Selection**

* **Offline Support**: Only the SAPI engine operates entirely offline. We plan to support other future engines that do have offline support. Note that we do cache data, which can help.
* **API Keys**: You'll need to obtain API keys for Azure and Google TTS. [Learn how to get them here](getting-keys-for-azure-or-google.md).
* **gTTS**: This is a free but limited option. Your target language determines the voice and language in translation. This works because it uses the voice found in the [Google Translate](https://translate.google.com) tool online. We don't use the translation service - just the voice. So, not all languages are supported.

**Data Collection**

* **Minimal Tracking**: We collect basic usage statistics but do not personally identify users.
* **Transparency**: [View our code here](https://github.com/AceCentre/TranslateAndTTS/blob/05e1f68e287ef5a653aaeb2e21d2e89f4f7a3d85/utils.py#L271) to see the exact data we collect.

**Translation Services**

* **Setting Languages**: The most crucial step is to set both the **Writing** and **Target** languages.
* **Free Tier**: The default free service is [myMemory](http://mymemory.translated.net). You can switch to a paid service if you find it lacking for your language pair.
* **Paid Tier**: [DeepL](https://www.deepl.com/translator) offers comprehensive language coverage and is highly recommended. But you may want to try the others.
* **AAC Software Integration**: To make the translated string available in your AAC software, check the box to overwrite the clipboard.

You can edit the settings file by hand if you wish. To do this, navigate to `%AppData%\TranslateAndTTS` in File Explorer to find the `settings.cfg` file. Edit the configuration using either a plain text editor.

**Note: You can copy this settings file and have numerous versions of them - or make it and distribute it to an end user. You would use the `--config file path to run the application using a different config file.cfg` parameter**

#### Step 4. Add your support to your AAC software.

See [the specific guides](aac-guides.md) for your AAC software but in short;

* Add a button to _copy_ the message bar (writing area)
* Then, have an action on this button to call the executable found at `%UserProfile%\AppData\Local\Programs\Ace Centre\TranslateAndTTS\` (**Note: You will need to browse for the app. You can paste this link into the file explorer but you need to find the exact path on your own computer)**
* Then it's wise to wait around 5-10 seconds (and if translating text)
* Clear the message bar
* Paste the returning text back if you are translating

You can test it by copying some text from a text file and running the app. Give it a go.
