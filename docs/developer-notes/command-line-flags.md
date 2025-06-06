# Command Line Flags

#### The app (client.exe) is designed to be called by a AAC application - and relies on some text being available in the copy buffer. You can use these parameters/flags to control aspects like which settings file is loaded or other aspects. Read below for all the flags.&#x20;

#### General Usage

```
client.exe [options]
```

#### Options

| Flag                 | Description                                         | Type   | Required | Default | Example                           |
| -------------------- | --------------------------------------------------- | ------ | -------- | ------- | --------------------------------- |
| `-s, --style`        | Specifies the voice style for Azure Text-to-Speech. | String | No       | None    | `--style "sad"`                   |
| `-sd, --styledegree` | Specifies the degree of the style for Azure TTS.    | Float  | No       | None    | `--styledegree 1.5`               |
| `-c, --config`       | Path to a defined config file .                     | String | No       | None    | `--config "C:\somepath\some.cfg"` |
| `-l, --listvoices`   | List Voices to see what's available                 | Bool   | No       | None    |                                   |
| `-p, --preview`      | Only preview the voice                              | Bool   | No       | None    |                                   |
| `-t, --text`         | Text to speak (if not provided, uses clipboard)     | String | No       | None    | `--text "Hello world"`            |

### Using the style flag for Azure voices

You can use the command line's `--style` flag for Azure voices. If you do this, follow it with one of these style flags. You can change the strength of these with `--styledegree` being 0.1 to 2. By default it is 1. So 2 would double it. Be warned. Some voices don't have all styles. [Read the Azure docs for more info](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-voice#use-speaking-styles-and-roles).

|                             |                       |                        |
| --------------------------- | --------------------- | ---------------------- |
| advertisement\_upbeat       | affectionate          | angry                  |
| assistant                   | calm                  | chat                   |
| cheerful                    | customerservice       | depressed              |
| disgruntled                 | documentary-narration | embarrassed            |
| empathetic                  | envious               | excited                |
| fearful                     | friendly              | gentle                 |
| hopeful                     | lyrical               | narration-professional |
| narration-relaxed           | newscast              | newscast-casual        |
| newscast-formal             | poetry-reading        | sad                    |
| serious                     | shouting              | sports\_commentary     |
| sports\_commentary\_excited | whispering            | terrified              |
| unfriendly                  |                       |                        |

## CLI Configuration Tool

The CLI Configuration Tool (`Configure AACSpeakHelper CLI.exe` or `cli_config_creator.py` in development) provides an interactive way to configure AACSpeakHelper.

### Usage

**Development:**
```bash
uv run python cli_config_creator.py [--config path/to/settings.cfg]
```

**Installed version:**
Run "Configure AACSpeakHelper CLI" from the Start Menu, or:
```bash
"Configure AACSpeakHelper CLI.exe" [--config path/to/settings.cfg]
```

### CLI Configuration Options

The CLI tool provides a menu-driven interface with these options:

1. **Configure TTS Engine** - Set up text-to-speech engines
   - Choose from Sherpa-ONNX, Azure TTS, Google TTS, and others
   - Configure voice settings, rate, volume
   - Set up API keys for cloud services

2. **Configure Translation** - Set up translation services
   - Choose translation provider (Google, Microsoft, DeepL, etc.)
   - Set source and target languages
   - Configure API credentials

3. **View Current Configuration** - Display current settings

4. **Save and Exit** - Save changes and exit

5. **Exit without Saving** - Exit without saving changes

### Configuration File Management

The CLI tool automatically:
- Loads existing configuration from the default location
- Creates default configuration if none exists
- Supports custom configuration file paths with `--config` parameter
- Saves configuration in the appropriate location based on installation type
