# Configure

After installation, you need to configure the application. There are two main ways to configure AACSpeakHelper:

1. **CLI Configuration Tool** - Use our command-line configuration tool `Configure AACSpeakHelper CLI` (recommended)
2. **Manual Editing** - Edit the settings file by hand using a text editor

## Using the CLI Configuration Tool

The easiest way to configure AACSpeakHelper is using our CLI configuration tool. You can find **`Configure AACSpeakHelper CLI`** in your start menu after installation, or run it directly from the installation directory.

The CLI tool provides an interactive menu with the following options:

1. **Configure TTS Engine** - Set up your Text-to-Speech engine and voice
2. **Configure Translation** - Set up translation settings and language pairs
3. **Configure Transliteration** - Set up script conversion settings (e.g., Latin to Devanagari)
4. **View Current Configuration** - Review your current settings
5. **Save and Exit** - Save your changes and exit
6. **Exit without Saving** - Exit without saving changes

### Configuring TTS Engine

When you select option 1, you'll be able to choose from several Text-to-Speech engines:

#### Available TTS Engines

**Sherpa-ONNX** (Recommended for most users)
- Offline TTS engine that works without internet
- Supports a large range of languages not supported by other systems
- Good balance of quality and performance
- No API keys required

**Azure TTS** (High quality, requires API key)
- Microsoft's cloud-based TTS service
- Excellent voice quality and natural speech
- Requires Azure Speech Services subscription and API key
- Supports many languages and voices

**Google TTS** (High quality, requires API key)
- Google's cloud-based TTS service
- High-quality voices with natural intonation
- Requires Google Cloud TTS API credentials
- Wide language support

**Google Trans TTS** (Free, limited quality)
- Free TTS using Google Translate
- No API key required but limited quality
- May have usage restrictions

**Other Premium Engines Available:**
- **ElevenLabs** - Premium quality voices, requires subscription
- **PlayHT** - High quality voices, requires subscription
- **AWS Polly** - Good quality, requires AWS account
- **IBM Watson** - Good quality, requires IBM Cloud account
- **OpenAI TTS** - High quality, requires OpenAI API key

{% hint style="info" %}
**Important Notes:**
- Sherpa-ONNX works offline but requires internet during initial setup to download voice models
- Each Sherpa-ONNX model is around 250MB and may take time to download
- First-time speech generation may be slower as models initialize
- TTS voices work best with text in the correct script/language (e.g., Arabic voices need Arabic text)
{% endhint %}

#### TTS Configuration Options

When configuring a TTS engine, you'll be prompted for:

**Voice ID** - The specific voice to use (varies by engine and language)
**Rate** - Speech speed (0 = normal, negative values = slower, positive = faster)
**Volume** - Audio volume (100 = normal, 50 = quieter, 150 = louder)
**Save Audio File** - Whether to save audio files to disk for caching and reuse
**Bypass TTS** - Skip text-to-speech entirely (useful for translation-only mode)

### Configuring Translation

When you select option 2 from the main menu, you can configure translation settings:

#### Translation Providers

**GoogleTranslator** (Free, limited usage)
- Free translation service using Google Translate
- May have usage limits or temporary blocks with heavy use
- Good for testing and light usage

**Microsoft Translator** (Requires API key)
- High-quality translation service
- Requires Azure Translator subscription
- More reliable for production use

**Other Translation Providers Available:**
- DeepL (Premium quality, requires API key)
- Yandex Translator
- Baidu Translator
- LibreTranslate
- MyMemory Translator

#### Translation Settings

**No Translate** - Disable translation entirely if your text is already in the target language
**Start Language** - The language of your input text (e.g., "en" for English)
**End Language** - The target language for translation (e.g., "ps" for Pashto)
**Replace Pasteboard** - Whether to replace clipboard content with translated text

### Configuring Transliteration

When you select option 3 from the main menu, you can configure transliteration settings:

#### What is Transliteration?

Transliteration converts text from one script to another while maintaining the same language. For example, converting Latin script "namaste" to Devanagari script "नमस्ते" (both are Hindi, just different scripts).

#### Transliteration Settings

**No Transliterate** - Enable or disable transliteration entirely
**Language** - The language for transliteration (Hindi, Arabic, Bengali, etc.)
**From Script** - The source script (e.g., "Latn" for Latin)
**To Script** - The target script (e.g., "Deva" for Devanagari)
**Replace Pasteboard** - Whether to replace clipboard content with transliterated text

#### Supported Languages and Scripts

- **Arabic** (ar) - Latin ↔ Arabic script
- **Bengali** (bn) - Latin ↔ Bengali script
- **Gujarati** (gu) - Latin ↔ Gujarati script
- **Hindi** (hi) - Latin ↔ Devanagari script
- **Kannada** (kn) - Latin ↔ Kannada script
- **Malayalam** (ml) - Latin ↔ Malayalam script
- **Marathi** (mr) - Latin ↔ Devanagari script
- **Oriya** (or) - Latin ↔ Oriya script
- **Punjabi** (pa) - Latin ↔ Gurmukhi script
- **Tamil** (ta) - Latin ↔ Tamil script
- **Telugu** (te) - Latin ↔ Telugu script
- **Urdu** (ur) - Latin ↔ Arabic script

#### Requirements

Transliteration requires Azure Translator credentials:
- Azure Translator subscription key
- Azure resource region (e.g., "uksouth", "eastus")

These can be configured in your settings file or through environment variables.

## Manual Configuration

If you prefer to edit configuration files directly, you can manually edit the `settings.cfg` file.

### Location of Settings File

**For installed versions:**
Navigate to `%AppData%\Ace Centre\AACSpeakHelper` in File Explorer to find the `settings.cfg` file.

**For development versions:**
The `settings.cfg` file is located in the project root directory.

### Editing the Settings File

You can edit the configuration file using any plain text editor (Notepad, VS Code, etc.). The file uses INI format with sections and key-value pairs.

#### Example Configuration Structure

```ini
[App]
collectstats = True

[translate]
no_translate = False
start_lang = en
end_lang = ps
replace_pb = True
provider = GoogleTranslator

[transliterate]
no_transliterate = True
language = hi
from_script = Latn
to_script = Deva
replace_pb = True

[TTS]
engine = azureTTS
bypass_tts = False
save_audio_file = True
rate = 0
volume = 100

[azureTTS]
key = your-azure-key-here
location = uksouth
voice_id = en-US-JennyNeural
```

### Using Custom Configuration Files

You can create multiple configuration files for different use cases:

**Command Line Usage:**
```bash
client.exe --config path/to/your/custom-settings.cfg
```

**Distribution to End Users:**
You can create pre-configured settings files and distribute them to users. This is useful for organizations that want to deploy AACSpeakHelper with specific settings.

### Configuration File Sections

**[App]** - Application settings
- `collectstats` - Whether to collect anonymous usage statistics

**[translate]** - Translation settings
- `no_translate` - Disable translation (True/False)
- `start_lang` - Source language code (e.g., "en")
- `end_lang` - Target language code (e.g., "ps")
- `replace_pb` - Replace clipboard content (True/False)
- `provider` - Translation provider name

**[transliterate]** - Transliteration settings
- `no_transliterate` - Disable transliteration (True/False)
- `language` - Language code for transliteration (e.g., "hi")
- `from_script` - Source script code (e.g., "Latn")
- `to_script` - Target script code (e.g., "Deva")
- `replace_pb` - Replace clipboard content (True/False)

**[TTS]** - Text-to-Speech settings
- `engine` - TTS engine name (e.g., "azureTTS", "Sherpa-ONNX")
- `bypass_tts` - Skip TTS entirely (True/False)
- `save_audio_file` - Cache audio files (True/False)
- `rate` - Speech rate (0 = normal)
- `volume` - Audio volume (100 = normal)
- `voice_id` - Voice identifier

**Engine-specific sections** (e.g., [azureTTS], [googleTTS])
- Contains API keys, credentials, and engine-specific settings
