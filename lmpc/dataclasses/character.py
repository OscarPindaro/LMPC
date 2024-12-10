from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict
from pathlib import Path
import re


# Define an enum for character alignment
class Alignment(Enum):
    LAWFUL_GOOD = "Lawful Good"
    NEUTRAL_GOOD = "Neutral Good"
    CHAOTIC_GOOD = "Chaotic Good"
    LAWFUL_NEUTRAL = "Lawful Neutral"
    TRUE_NEUTRAL = "True Neutral"
    CHAOTIC_NEUTRAL = "Chaotic Neutral"
    LAWFUL_EVIL = "Lawful Evil"
    NEUTRAL_EVIL = "Neutral Evil"
    CHAOTIC_EVIL = "Chaotic Evil"


# Define a dataclass for an opinion
@dataclass
class Opinion:
    title: str
    content: str

    def __repr__(self):
        capped_content = (
            (self.content[:75] + "...") if len(self.content) > 75 else self.content
        )
        return f"Opinion(title='{self.title}', content='{capped_content}')"

    def to_markdown(self) -> str:
        return f"### {self.title}\n{self.content}\n"


# Define a dataclass for a character
@dataclass
class Character:
    name: str
    origin_story: str
    alignment: Alignment
    values: List[str]
    objectives: List[str]
    opinions: List[Opinion]

    def to_text(self) -> str:
        text = ""
        text += f"# {self.name}\n\n"
        text += f"## Origin Story\n\n{self.origin_story}\n\n"
        text += f"## Alignment\n\n{self.alignment.value}\n\n"
        text += "## Values\n\n"
        for value in self.values:
            text += f"- {value}\n"
        # after values, add an additional newline
        text += "\n"
        text += "## Objectives\n\n"
        for objective in self.objectives:
            text += f"- {objective}\n"
        text += "\n"
        text += "## Opinions\n\n"
        for opinion in self.opinions:
            text += f"### {opinion.title}\n{opinion.content}\n\n"
        return text

    def save_to_markdown(self, file_path: Path):
        """Save the character to a markdown file."""
        file_path = Path(file_path)
        file_path.write_text(self.to_text())

    @staticmethod
    def from_text(text: str) -> "Character":
        lines = text.splitlines()

        name = lines[0].strip("# \n")
        origin_story = ""
        alignment = None
        values = []
        objectives = []
        opinions = []
        current_section = None
        current_opinion_title = None
        current_opinion_description = ""

        for line in lines[1:]:
            line = line.strip()
            if line.startswith("## "):
                current_section = line.strip("# \n")
            elif line.startswith("### "):
                if current_opinion_title:
                    opinions.append(
                        Opinion(
                            title=current_opinion_title,
                            content=current_opinion_description.strip(),
                        )
                    )
                current_opinion_title = line.strip("# \n")
                current_opinion_description = ""
            elif current_section == "Origin Story":
                origin_story += line + "\n"
            elif current_section == "Alignment":
                if alignment is None:
                    alignment = Alignment[line.replace(" ", "_").upper()]
            elif current_section == "Values":
                if line.startswith("- "):
                    values.append(line.strip("- "))
            elif current_section == "Objectives":
                if line.startswith("- "):
                    objectives.append(line.strip("- "))
            elif current_section == "Opinions":
                current_opinion_description += line + "\n"

        if current_opinion_title:
            opinions.append(
                Opinion(
                    title=current_opinion_title,
                    content=current_opinion_description.strip(),
                )
            )

        return Character(
            name=name,
            origin_story=origin_story.strip(),
            alignment=alignment,
            values=values,
            objectives=objectives,
            opinions=opinions,
        )

    @staticmethod
    def load_from_markdown(file_path: Path | str) -> "Character":
        """Load a character from a markdown file."""
        file_path = Path(file_path)
        content = file_path.read_text()
        return Character.from_text(content)

    def __repr__(self):
        capped_origin_story = (
            (self.origin_story[:75] + "...")
            if len(self.origin_story) > 75
            else self.origin_story
        )
        capped_values = [
            value[:75] + "..." if len(value) > 75 else value for value in self.values
        ]
        capped_objectives = [
            objective[:75] + "..." if len(objective) > 75 else objective
            for objective in self.objectives
        ]
        return (
            f"Character(name='{self.name}', origin_story='{capped_origin_story}', alignment='{self.alignment.value}', "
            f"values_count={len(self.values)}, values={capped_values}, "
            f"objectives_count={len(self.objectives)}, objectives={capped_objectives}, "
            f"opinions_count={len(self.opinions)})"
        )
