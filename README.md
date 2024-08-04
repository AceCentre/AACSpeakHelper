# AAC Online Speak & Translate Plug-in for Windows ("AAC Speak Helper")

<img src='https://raw.githubusercontent.com/AceCentre/TranslateAndTTS/main/assets/translatepb.png' alt="Blue logo with translate icon" width="200">

## For Full Documentation see here https://docs.acecentre.org.uk/products/v/aac-speak-helper-tool/ 

## Introduction

AAC Speak Helper is designed to enhance your ability to communicate. It leverages the copy-paste clipboard to offer translation services in various languages. It uses multiple providers' Text-to-Speech (TTS) technology to read aloud the translated text. You can easily configure all these functionalities through our Configure app and maintain numerous settings files for different tasks.

## Use Case

Imagine you are a Ukrainian speaker with limited English skills residing in a care facility. AAC Speak Helper bridges you and your caregivers, translating Ukrainian text into English. Moreover, it supports people who need to speak languages less commonly supported by TTS technology.

[![Overview Video](https://cdn.loom.com/sessions/thumbnails/dcd185df50224279a0c2630b6ca6b04f-1694639990490-with-play.gif)](https://www.loom.com/share/dcd185df50224279a0c2630b6ca6b04f)

## Compatibility

AAC Speak Helper is a lightweight Windows executable. It can be called from any AAC app on Windows that can run external programs.

## How it Works

AAC Speak Helper reads the text once the text is copied to the clipboard (using Ctrl+C). Depending on the configuration settings, it either translates the text using the selected service, speaks it aloud, or reads it. There are additional features, such as putting intonation (or style) onto some voices. We have a graphical application that can configure the app. The main application, though, has no interface. 

## Developer details

see [this mermaid graph](https://www.mermaidchart.com/raw/bc383b62-6f3e-47de-b168-90786a151ea5?theme=light&version=v0.1&format=svg)

![Overview of project](./assets/developer-overview.png)

See build details [here](https://github.com/AceCentre/TranslateAndTTS/blob/main/.github/workflows/windows-build-release.yml). 

```bash
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

then run the server

```bash
python AACSpeakHelper.py
```

add some text to your buffer and run 

```bash
python client.py
```
Running the GUI can be fun. 


## Troubleshooting

As this is a quick prototype, it may have some issues. For issues regarding connectivity or functionality, please note that Azure, Google Cloud and translation services require an online connection. If you have any questions, suggestions, or contributions, please create a pull request or [donate](https://acecentre.org.uk/get-involved/donate).

