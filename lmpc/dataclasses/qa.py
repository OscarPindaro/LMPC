from dataclasses import dataclass

@dataclass
class QAPair:
    instruction: str 
    query: str
    answer: str