from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os
from typing import Any, Optional
from dotenv import load_dotenv

load_dotenv()

class BaseGroqModel:
    def __init__(
        self,
        model_name: str = "llama3-8b-8192",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
    ):
        self.model = ChatGroq(
            model_name=model_name,
            temperature=temperature,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            max_tokens=max_tokens,
            top_p=top_p
        )

    def __call__(self, prompt: str, *args: Any, **kwargs: Any) -> str:
        response = self.model.invoke(prompt)
        return response.content

    def build_messages(self, prompt: str) -> list[dict]:
        """
        Helper method to build message format if needed
        """
        return [{"role": "user", "content": prompt}]
