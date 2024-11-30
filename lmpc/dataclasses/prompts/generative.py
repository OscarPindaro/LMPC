from dataclasses import dataclass
from typing import List

@dataclass
class GenerativePrompt:
    persona: str
    instruction: str
    examples: List[str]

