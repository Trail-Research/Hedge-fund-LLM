from abc import ABC, abstractmethod
from .base_models import BaseGroqModel

class BaseAgent(ABC):
    def __init__(self, temperature: float = 0.7):
        self.model = BaseGroqModel(temperature=temperature)
    
    @abstractmethod
    def build_prompt(self, *args, **kwargs) -> str:
        """Build the prompt for the agent"""
        pass
    
    def invoke(self, *args, **kwargs) -> str:
        """Execute the agent's task"""
        prompt = self.build_prompt(*args, **kwargs)
        return self.model(prompt) 