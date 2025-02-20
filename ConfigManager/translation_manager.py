# File: translation_manager.py
from deep_translator import GoogleTranslator


class TranslationManager:
    @staticmethod
    def get_providers():
        return ["google", "microsoft", "deepl"]

    def test_translation(self, provider, text):
        translator = GoogleTranslator(source="auto", target="en")
        return translator.translate(text)
