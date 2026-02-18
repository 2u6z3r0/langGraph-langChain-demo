import os

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} is not set. Add it in your .env file.")
    return value


def content_to_text(content: object) -> str:
    """Normalize LangChain message content into plain text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
                else:
                    parts.append(str(item))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    return str(content)


def get_llm(temperature: float = 0.2) -> BaseChatModel:
    """Create a chat model from env vars (gemini/openai/deepseek)."""
    load_dotenv()
    provider = os.getenv("LLM_PROVIDER", "gemini").strip().lower()
    override_model = os.getenv("LLM_MODEL")

    if provider == "gemini":
        api_key = _require_env("GOOGLE_API_KEY")
        model = override_model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        return ChatGoogleGenerativeAI(
            model=model, temperature=temperature, google_api_key=api_key
        )

    if provider == "openai":
        api_key = _require_env("OPENAI_API_KEY")
        model = override_model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return ChatOpenAI(
            model=model, temperature=temperature, api_key=SecretStr(api_key)
        )

    if provider == "deepseek":
        api_key = _require_env("DEEPSEEK_API_KEY")
        model = override_model or os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=SecretStr(api_key),
            base_url=base_url,
        )

    raise ValueError("Invalid LLM_PROVIDER. Use one of: gemini, openai, deepseek.")
