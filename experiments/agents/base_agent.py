# agents/base_agent.py

from typing import List, Callable, Any
import logging

class BaseAgent:
    def __init__(self, name: str, instructions: str, functions: List[Callable[..., Any]]):
        self.name = name
        self.instructions = instructions
        self.functions = functions
        self.logger = logging.getLogger(self.name)

    def handle(self, context_variables, *args, **kwargs):
        """
        Handle a user request by invoking the appropriate function based on context.
        This method can be overridden by subclasses if needed.
        """
        for func in self.functions:
            result = func(context_variables, *args, **kwargs)
            if result:
                return result
        return None
