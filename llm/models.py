"""
LLM model configuration and initialization.
"""
from agno.models.google import Gemini


def initialize_gemini_model(api_key: str, model_id: str = "gemini-2.5-flash") -> Gemini:
    """
    Initialize and return a Gemini LLM instance.
    
    Args:
        api_key: Google API key
        model_id: Model identifier (default: gemini-2.5-flash)
    
    Returns:
        Initialized Gemini model instance
    """
    return Gemini(id=model_id, api_key=api_key)
