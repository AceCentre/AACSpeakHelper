# File: language_manager.py
import langcodes
from typing import List

class LanguageManager:
    @staticmethod
    def get_language_name(code: str) -> str:
        return langcodes.Language.get(code).display_name()
    
    @staticmethod
    def search_languages(query: str) -> List[str]:
        try:
            lang = langcodes.find(query)
            return [lang.to_tag()]
        except:
            return [] 