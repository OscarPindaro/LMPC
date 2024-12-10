from dataclasses import dataclass, field
from typing import Any, Dict, List
import json
from pathlib import Path


@dataclass
class QAPair:
    instruction: str
    question: str
    answer: str
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instruction": self.instruction,
            "question": self.question,
            "answer": self.answer,
            "meta": self.meta,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "QAPair":
        return QAPair(
            instruction=data["instruction"],
            question=data["question"],
            answer=data["answer"],
            meta=data.get("meta", {}),
        )

    def to_json_str(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @staticmethod
    def from_json_str(json_str: str) -> "QAPair" | List["QAPair"]:
        if isinstance(json_str, str):
            data = json.loads(json_str)
            if isinstance(data, list):
                return [QAPair.from_dict(item) for item in data]
            return QAPair.from_dict(data)
        raise ValueError("Input must be a JSON string")

    @staticmethod
    def to_json_list_str(qa_pairs: List["QAPair"]) -> str:
        return json.dumps([qa.to_dict() for qa in qa_pairs], indent=2)

    # Add these methods to the QAPair class
    def to_json(self, path: Path) -> None:
        """Write QAPair to a JSON file"""
        path = Path(path)
        path.write_text(self.to_json())

    @staticmethod
    def from_json(path: Path) -> "QAPair" | List["QAPair"]:
        """Read QAPair(s) from a JSON file"""
        path = Path(path)
        json_str = path.read_text()
        return QAPair.from_json_str(json_str)

    @staticmethod
    def to_json_list(qa_pairs: List["QAPair"], path: Path) -> None:
        """Write list of QAPairs to a JSON file"""
        path = Path(path)
        path.write_text(QAPair.to_json_list_str(qa_pairs))
