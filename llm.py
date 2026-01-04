from langchain.chat_models import init_chat_model
from config import LLM_SETTINGS

model_settings = LLM_SETTINGS

model = init_chat_model(
    model=model_settings["model"],
    model_provider=model_settings["provider"],
    api_key=model_settings["api_key"],
    temperature=model_settings["temperature"])