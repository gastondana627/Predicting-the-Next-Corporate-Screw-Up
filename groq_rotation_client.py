import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union
from urllib import error, request

from dotenv import load_dotenv

try:
    from google import genai as google_genai
except Exception:  # pragma: no cover - optional dependency
    google_genai = None


class AdaptiveGroqClient:
    """A provider-aware LLM client that uses Groq first and fails over to Gemini/OpenRouter."""

    def __init__(
        self,
        model: str = "llama-3.3-70b-versatile",
        base_url: str = "https://api.groq.com/openai/v1",
        env_path: Optional[Union[str, Path]] = None,
        provider_order: Optional[Sequence[str]] = None,
        max_attempts: int = 3,
        timeout: int = 60,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.max_attempts = max_attempts
        self.timeout = timeout
        self.logger = logger or logging.getLogger("adaptive_groq_client")

        load_dotenv(dotenv_path=env_path or ".env", override=False)
        self.providers = {
            "groq": os.getenv("GROQ_API_KEY"),
            "gemini": os.getenv("GEMINI_API_KEY"),
            "openrouter": os.getenv("OPENROUTER_API_KEY"),
        }

        ordered_providers = []
        for provider in (provider_order or ["groq", "gemini", "openrouter"]):
            if provider in self.providers and self.providers[provider]:
                ordered_providers.append(provider)

        if not ordered_providers:
            raise ValueError("No API keys were found. Expected GROQ_API_KEY, GEMINI_API_KEY, and/or OPENROUTER_API_KEY in the environment.")

        self.provider_order = ordered_providers

    def _build_messages(self, prompt: str, system_prompt: Optional[str] = None) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return messages

    def _headers(self, api_key: str) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def _normalize_response(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return payload

    def _call_groq(self, messages: Sequence[Dict[str, Any]], **options: Any) -> Dict[str, Any]:
        api_key = self.providers["groq"]
        body: Dict[str, Any] = {"model": self.model, "messages": list(messages)}
        body.update(options)
        req = request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers=self._headers(api_key),
            method="POST",
        )
        with request.urlopen(req, timeout=self.timeout) as response:
            return self._normalize_response(json.loads(response.read().decode("utf-8")))

    def _call_gemini(self, messages: Sequence[Dict[str, Any]], **options: Any) -> Dict[str, Any]:
        api_key = self.providers["gemini"]
        prompt_text = "\n".join([item.get("content", "") for item in messages if item.get("role") != "system"])

        if google_genai is not None:
            client = google_genai.Client(api_key=api_key)
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt_text)
            content = getattr(response, "text", "") or ""
            return {"choices": [{"message": {"role": "assistant", "content": content}}]}

        payload = {
            "contents": [{"parts": [{"text": prompt_text}]}],
            **({"generationConfig": options} if options else {}),
        }
        req = request.Request(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=self.timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
            candidates = data.get("candidates", [])
            content = ""
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                content = "".join(part.get("text", "") for part in parts)
            return {"choices": [{"message": {"role": "assistant", "content": content}}]}

    def _call_openrouter(self, messages: Sequence[Dict[str, Any]], **options: Any) -> Dict[str, Any]:
        api_key = self.providers["openrouter"]
        body: Dict[str, Any] = {
            "model": options.pop("model", "openai/gpt-4o-mini"),
            "messages": list(messages),
        }
        body.update(options)
        req = request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/gastondana627/Predicting-the-Next-Corporate-Screw-Up",
                "X-Title": "RiskBot",
            },
            method="POST",
        )
        with request.urlopen(req, timeout=self.timeout) as response:
            return self._normalize_response(json.loads(response.read().decode("utf-8")))

    def complete(self, prompt: str, *, system_prompt: Optional[str] = None, **options: Any) -> Dict[str, Any]:
        messages = self._build_messages(prompt, system_prompt)
        errors: List[tuple[str, Exception]] = []

        for provider_name in self.provider_order:
            try:
                if provider_name == "groq":
                    return self._call_groq(messages, **options)
                if provider_name == "gemini":
                    return self._call_gemini(messages, **options)
                if provider_name == "openrouter":
                    return self._call_openrouter(messages, **options)
            except (error.HTTPError, error.URLError, TimeoutError, ConnectionError, json.JSONDecodeError, KeyError, ValueError) as exc:
                self.logger.warning("Provider %s failed: %s", provider_name, exc)
                errors.append((provider_name, exc))
                continue

        raise RuntimeError(f"All providers failed: {errors[-1][0]} -> {errors[-1][1]}") if errors else RuntimeError("No providers available")


def load_keys_from_env(env_path: Optional[Union[str, Path]] = None) -> Dict[str, str]:
    load_dotenv(dotenv_path=env_path or ".env", override=False)
    return {
        "groq": os.getenv("GROQ_API_KEY", ""),
        "gemini": os.getenv("GEMINI_API_KEY", ""),
        "openrouter": os.getenv("OPENROUTER_API_KEY", ""),
    }


def create_client(**kwargs: Any) -> AdaptiveGroqClient:
    return AdaptiveGroqClient(**kwargs)


if __name__ == "__main__":
    client = create_client(env_path=".env")
    print(f"Loaded providers: {', '.join(client.provider_order)}")
