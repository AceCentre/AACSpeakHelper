# Troubleshooting and Feature requests

As this is a quick prototype, it may have some issues. For issues regarding connectivity or functionality, please note that Azure, Google Cloud and translation services require an online connection. If you have any questions, suggestions, or contributions, please create a pull request or [donate](https://acecentre.org.uk/get-involved/donate).

## Common Feature requests

* Offline Translation. Although possible with NLLB (Meta) its not easy to do all the language pairs we potentially need.&#x20;
* The key feature is to make the integration easier. This is actually best done if it was a system wide voice rather than all software having to integrate different providers. So how do we do it? See our roadmap&#x20;
* ElevenLabs access.&#x20;
* Offline Azure/Google etc voices. Although advertised as kind of possible its not without limitations (notably not all voices are available like this from Microsoft and particularly not those that are of high need becauser we dont have much language support)

## Roadmap



```mermaid
gantt
    title Software Project Roadmap
    dateFormat  YYYY-MM-DD
    section Copy/Paste Speech and Translation Engine
    Design & Planning        :done, des1, 2024-07-01, 2024-08-01
    Development              :done, dev1, 2024-08-02, 2024-09-30
    Testing & Refinement     :active, test1, 2024-10-01, 2024-10-15
    Release                  : milestone, rel1, 2024-10-15, 1d
    
    section SAPI and iOS/Android TTS Bridges (Pending Funding)
    Research & Framework Selection :done, res1, 2024-09-01, 2024-09-30
    SAPI Bridge Development (On Hold)    :crit, dev2, after rel1, 60d
    iOS Bridge Development (On Hold)     :crit, dev3, after dev2, 60d
    Android Bridge Development (On Hold) :crit, dev4, after dev3, 60d
    Testing and Integration (On Hold)    :crit, test2, after dev4, 30d
    Release (Pending)                    : milestone, rel2, after test2, 1d
    
    section Project VoiceGarden (Pending Funding)
    Project Scoping            : done, proj1, 2024-09-15, 2024-09-30
    Phase 1 Trial (Pending Funding)      :crit, dev5, after proj1, 120d
    Phase 2 Trial (Pending Funding)      :crit, coll1, after dev5, 120d
    Public Beta (Pending)                : milestone, beta1, after coll1, 1d
    Final Release (Pending)              : milestone, rel3, after beta1, 60d
```
