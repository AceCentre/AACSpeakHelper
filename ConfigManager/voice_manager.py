from typing import List, Optional
from dataclasses import dataclass
import langcodes
from py3_tts_wrapper import TTSFactory, TTSEngine

@dataclass
class VoiceInfo:
    id: str
    name: str
    language: str
    gender: str
    engine: str
    is_downloaded: bool = False

class VoiceManager:
    def __init__(self, tts_engine: TTSEngine):
        self.engine = tts_engine
        self.voices: List[VoiceInfo] = []
        self.load_voices()
        
    def load_voices(self):
        """Load voices from engine and convert to VoiceInfo objects"""
        raw_voices = self.engine.get_voices()
        self.voices = [
            VoiceInfo(
                id=v.get('id'),
                name=v.get('name'),
                language=v.get('language'),
                gender=v.get('gender', 'neutral'),
                engine=self.engine.__class__.__name__,
                is_downloaded=v.get('is_downloaded', True)
            )
            for v in raw_voices
        ]
        
    def search_voices(self, query: str) -> List[VoiceInfo]:
        """Search voices using langcodes"""
        try:
            lang = langcodes.find(query)
            matches = []
            
            for voice in self.voices:
                # Match language code
                if lang.matches(voice.language):
                    matches.append(voice)
                    continue
                    
                # Match display name
                voice_lang = langcodes.Language.get(voice.language)
                if query.lower() in voice_lang.display_name().lower():
                    matches.append(voice)
                    continue
                    
                # Match voice name
                if query.lower() in voice.name.lower():
                    matches.append(voice)
                    
            return matches
            
        except Exception:
            # If language lookup fails, do basic string matching
            return [v for v in self.voices 
                   if query.lower() in v.name.lower() 
                   or query.lower() in v.language.lower()] 