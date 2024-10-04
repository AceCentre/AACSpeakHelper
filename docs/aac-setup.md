# AAC Setup

AACSpeakHelper ISNT a SAPI Speech engine. What this means is it is not seen by your AAC Software as a voice you would pick in your regular settings screen. We have to do some things to get this to work. And note you will have to be comfortable editing your software.&#x20;

In short you need to:

* Add a button to _copy_ the message bar (writing area)
* Then, have an action on this button to call the executable found at `%UserProfile%\AppData\Local\Programs\Ace Centre\AACSpeakHelper\client.exe` (**Note: You will need to browse for the app. You can paste this link into the file explorer but you need to find the exact path on your own computer)**
* Then it's wise to wait around 4-10 seconds&#x20;
* Clear the message bar
* Paste the returning text back if you are translating

You can test it by copying some text from a text file and running the app **client.exe**. Give it a go.

{% hint style="warning" %}
If you are not using translate you will need a keyboard in the right language. This can be tricky to make. Try using this  [http://aackeyboardmaker.streamlit.app](http://aackeyboardmaker.streamlit.app) - right now only supporting the Grid3. It certainly wont make complete keyboards but it will be a good starting point
{% endhint %}

### The Grid 3&#x20;

We make things a little easier for the Grid as we provide an example pageset with the correct path to the application on your desktop under "Example pagesets". You can double click this and then try it out. Write some text - and then press on the flag icon

### Tobii Dynavox Snap

<figure><img src=".gitbook/assets/AAC-Screen-Snap.jpg" alt=""><figcaption></figcaption></figure>

#### Communicator

See the demo pageset [here](https://github.com/AceCentre/TranslateAndTTS/tree/main/assets)

<figure><img src=".gitbook/assets/AAC-Screen-Communicator (1).png" alt=""><figcaption></figcaption></figure>

#### NuVoice

#### MindExpress

To-do

If you want to use mind-express for translation note that  MEX already can do this. See [here for a demo](https://www.jabbla.co.uk/vocab/translation-tool/)
