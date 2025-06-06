# How was this made

Blood, sweat and tears

We have

1. **A pipe server** (`AACSpeakHelperServer.py`)
   1. Reads in a config dict from settings.cfg
   2. Creates an object to the TTS Engine and holds it in memory to reduce coldstart time
   3. Speaks using sounddevice (heavily reliant on py3-tts-wrapper)
   4. Handles translation using various translation providers
   5. Communicates via named pipes with clients

2. **Client - calling executable** (`client.py`)
   1. You can pass it a config file path and text string
   2. If no text provided, it uses clipboard/pasteboard text
   3. Calls the pipe service to process text
   4. Supports command-line parameters for different configurations

3. **CLI Configuration Tool** (`cli_config_creator.py`)
   1. Interactive command-line interface for configuration
   2. Supports all TTS engines and translation providers
   3. Creates and manages settings.cfg files
   4. Replaces the unreliable GUI configuration tool

4. **Additional Tools**
   1. `CreateGridset.py` - Creates AAC communication grids
   2. `migrate_settings.py` - Migrates settings between versions


## Configuration Architecture

The application uses a multi-layered configuration approach:

1. **settings.cfg** - Main configuration file in INI format
   - Contains all TTS engine settings, translation settings, and application preferences
   - Located in `%AppData%\Ace Centre\AACSpeakHelper` for installed versions
   - Can be customized and distributed to end users

2. **config.enc** - Encrypted configuration for sensitive data
   - Contains API keys and credentials for cloud services
   - Generated during build process from environment variables
   - Provides fallback credentials when user hasn't configured their own

3. **Environment Variables** (Development only)
   - Used during development via .envrc files
   - Automatically encrypted into config.enc during build process

4. **Command-line Parameters**
   - Allow specifying custom configuration files
   - Enable different configurations for different use cases

## Technical Implementation

There is a lot of magic to make this work though. This includes

* [TTS-Wrapper ](https://github.com/willwade/tts-wrapper)- a unified wrapper to a range of TTS engines. This is needed as we need a unified way of get\_voices and speak, speak\_streamed etc
* [Sherpa-Onnx](https://github.com/k2-fsa/sherpa-onnx) - a really nice tooling pipleine to deal with VITS models that run on the edge.&#x20;
* [MMS](https://ai.meta.com/blog/multilingual-model-speech-recognition/) and [Models readied for Sherpa-Onnx](https://huggingface.co/willwade/mms-tts-multilingual-models-onnx) - Massive help this work from Meta - and we  converted their models for (Sherpa-)Onnx. We made some things on the way like a nice JSON with details on the voices. Commerical Providers: **Please note the licence these are under**
* QT/QT Threading. We had "fun" with threads. Never again will I do it like this
* Encryption in a github Action of keys and a hideous JSON file from Google. That wasted us a week.&#x20;

### Credits

* Will Wade (original v1, refactoring v2 several times, dealing with encryption, build scripts and generally pulling my hair out)
* Acer Jay Costillo (QT work and refactoring)
* Gavin Henderson - for making the call on baking in creds. I hated that and several times threw the idea out.&#x20;
* Simon Poole - CTO at Smartbox for making me aware of MMS.&#x20;

**Whats next?**

* SAPI Bridge. This is really what is needed. C++ developers - we need your help. See [Roadmap](../troubleshooting-and-feature-requests/roadmap.md)&#x20;
