class ConfigError(Exception):
    """Base class for configuration errors"""
    pass

class CredentialError(ConfigError):
    """Error related to credential handling"""
    pass

class VoiceError(ConfigError):
    """Error related to voice operations"""
    pass

class TranslationError(ConfigError):
    """Error related to translation operations"""
    pass 