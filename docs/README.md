# Introduction

{% embed url="https://youtu.be/mGgfczEWDvQ" %}
Basic, very short demo showing config and running
{% endembed %}

AACSpeakHelper is a small tool that enables you to\


* Take text written in a Windows AAC application&#x20;
* If you need to - Translate it using a choice of _online_ translation systems
* and if you need to - Speak that text using a range of online or new offline speech models supporting [1000's of languages](supported-languages.md) not currently supported by commercial providers

It is good if you&#x20;

* Want to set up a AAC system for someone speaking in a language not currently supported by solutions available
* If you have a client who wants to communicate to some people using a language they aren't familiar with. For example speaking to carers who are don't communicate using the communication aid users language or need to speak to family members who only speak in a language that they dont have a understanding of that written form

What its not good for

* Reading or saving long streams of text (eg reading a book aloud)
* If you want to use with a piece of software you cant copy the text from a message bar&#x20;
* You really have to use iOS, Android or something else

### Typical Use Cases

1. Language translation and speech output

Imagine you are a Kurdish speaker with limited English skills residing in a care facility. AAC Speak Helper bridges you and your caregivers, translating Kurdish text into English. Moreover, it supports people who need to speak languages less commonly supported by TTS technology.

2. Language not supported by current commercial solutions

If you speak Urdu - either as a bilingual speaker or as your primary language it can be difficult to find the perfect AAC system to meet your needs

### Compatibility

AAC Speak Helper is a lightweight Windows executable. It can be called from any AAC app on Windows that can run external programs.&#x20;

### How it Works

AAC Speak Helper reads the text once the text is copied to the clipboard (using Ctrl+C). Depending on the configuration settings, it either translates the text using the selected service, speaks it aloud, or reads it. There are additional features, such as putting intonation (or style) onto some voices. We have a graphical application that can configure the app. The main application, though, has no interface.
