# TranslateAndTTS

Copies the pasteboard. Translates to defined lang, Reads aloud and replaces pasteboard with translated text

## Who needs this

Imagine the scenario. You rely on technology to communicate, but you only speak in Ukranian and have little expressive skills in English. You are in a care setting. We need a quick translation tool using your existing technology to translate from your known language to English so you can communicate with your carers. This does that. 

![Short demo video](https://img.youtube.com/vi/c6zSPYZ4T10/maxresdefault.jpg)(https://www.youtube.com/watch?v=c6zSPYZ4T10)

## What does it work with?

It's a small windows executable. You call it from your Windows AAC app if it has a way of running external programs. Most Windows AAC apps can. 

## Where do I download it?

We have an installer - and we have a precompiled binary - which you can find [here](https://github.com/AceCentre/TranslateAndTTS/releases/latest). 

## How do I install it?

You need to unzip the folder, put it somewhere on your machine you can find again (e.g. C:\translatepb )

Next, you will need to edit the *settings.cfg* file

You can do this in a plain text editor such as Notepad. You may need to run the application as an Administrator depending on your rights. It Looks like this:

    [translate]
    # If you just want it to speak in the text you are writing mark this as True
    noTranslate = False
    # Note startLang isnt used 
    startLang = En
    # This is the key one - whats the target lang?
    endLang = Fr
    # Do you want to overwrite the pasteboard with the new translated string?
    replacepb = True
    [TTS]
    engine = gTTS
    # Engine = sapi5 (windows), coqui_ai_tts nsss (mac), espeak, gTTS
    voiceid = 'tts_models/nl/css10/vits'
    # VoiceID. To find what this would be run the programme with --listvoices 
    rate = 100
    volume = 100

Edit any of the items here - the essential one is what is your Start Language (What do you write in) - and what is your End Language? (What you want it translated to). See below for what Language codes are available. Note the TTS options. You can use SAPI - just make sure the VoiceID is listed. You can find this out by running the app with a flag of `--listvoices` in the command line. gTTS is using Google's TTS system. At this time you can't choose your voice - it will just pick the first one that matches the language code. We might change this at some point. 

*Note* - if you just want to use this tool to act as a bridge to the other TTS systems - mark noTranslate as True - and it will just read out the messaagebar text

Next, in your AAC software, you need to create a button. This button needs to 

1. Copy the message bar.
2. Call the application found in the folder you created earlier e.g `C:\translatepb\translatepb.exe`
3. Wait (e.g. 5-10 secs)
4. Paste (this pastes the translated text back into the message bar). You can look at this example gridset for some help 

## What if I have a problem?

Right now, this is a very, very quick (and dirty) example. We dare say there will be *SIGNIFICANT* problems using this. Remember if you use the gTTS option, it must be online. Translating too. We have put no logic in the script to deal with this failure. 

If you wish to improve the code and have the skills to, please fork and PR. Or consider [donating](https://acecentre.org.uk/get-involved/donate) to us and asking for specific support for this.

## Language codes available
 
- af: Afrikaans 
- ar: Arabic    
- bg: Bulgarian 
- bn: Bengali   
- bs: Bosnian   
- ca: Catalan   
- cs: Czech     
- da: Danish    
- de: German    
- el: Greek     
- en: English   
- es: Spanish   
- et: Estonian  
- fi: Finnish   
- fr: French    
- gu: Gujarati  
- hi: Hindi     
- hr: Croatian  
- hu: Hungarian 
- id: Indonesian
- is: Icelandic 
- it: Italian   
- iw: Hebrew    
- ja: Japanese  
- jw: Javanese
- km: Khmer
- kn: Kannada
- ko: Korean
- la: Latin
- lv: Latvian
- ml: Malayalam
- mr: Marathi
- ms: Malay
- my: Myanmar (Burmese)
- ne: Nepali
- nl: Dutch
- no: Norwegian
- pl: Polish
- pt: Portuguese
- ro: Romanian
- ru: Russian
- si: Sinhala
- sk: Slovak
- sq: Albanian
- sr: Serbian
- su: Sundanese
- sv: Swedish
- sw: Swahili
- ta: Tamil
- te: Telugu
- th: Thai
- tl: Filipino
- tr: Turkish
- uk: Ukrainian
- ur: Urdu
- vi: Vietnamese
- zh-CN: Chinese (Simplified)
- zh-TW: Chinese (Mandarin/Taiwan)
- zh: Chinese (Mandarin)

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

Don't bother - MEX already can do this. 

