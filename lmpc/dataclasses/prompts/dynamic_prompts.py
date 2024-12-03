from dataclasses import dataclass, field
from typing import List
from dynamicprompts.wildcards.wildcard_manager import WildcardManager
from dynamicprompts.generators import RandomPromptGenerator

from pathlib import Path


# Define a data class for dynamic generative prompts
@dataclass
class DynamicGenerativePrompt:
    # Attributes for dynamic prompts
    dynamic_persona: str
    dynamic_instruction: str
    dynamic_examples: List[str]

    # Optional attributes with default values
    seed: int = field(default=42)
    wildcard_dir: Path | None = field(default=None)
    wildcard_manager: WildcardManager | None = field(default=None, repr=False)
    random_prompt_generator: RandomPromptGenerator | None = field(
        default=None, repr=False
    )

    # Post-initialization to enforce constraints and initialize managers
    def __post_init__(self):
        # Ensure that both wildcard_dir and wildcard_manager are not set simultaneously
        if self.wildcard_dir is not None and self.wildcard_manager is not None:
            raise ValueError(
                "Both wildcard_dir and wildcard_manager cannot be set at the same time."
            )

        # Ensure that both wildcard_manager and random_prompt_generator are not set simultaneously
        if (
            self.wildcard_manager is not None
            and self.random_prompt_generator is not None
        ):
            raise ValueError(
                "Both wildcard_manager and random_prompt_generator cannot be set at the same time."
            )

        # Initialize wildcard_manager if wildcard_dir is provided
        if self.wildcard_dir is not None:
            self.wildcard_manager = WildcardManager(self.wildcard_dir)

        # Initialize random_prompt_generator if wildcard_manager is provided
        if self.random_prompt_generator is None:
            self.random_prompt_generator = RandomPromptGenerator(
                self.wildcard_manager, seed=self.seed
            )

    # Property to generate persona prompt
    @property
    def persona(self) -> str:
        return self.random_prompt_generator.generate(self.dynamic_persona)[0]

    # Property to generate instruction prompt
    @property
    def instruction(self) -> str:
        return self.random_prompt_generator.generate(self.dynamic_instruction)[0]

    # Property to generate examples prompt
    @property
    def examples(self) -> List[str]:
        to_ret: List[str] = [
            self.random_prompt_generator.generate(ex)[0] for ex in self.dynamic_examples
        ]
        return to_ret


from typing import List


def to_dynamic_prompt_string(choices: List[str]) -> str:
    to_ret = "{"
    for idx, c in enumerate(choices):
        to_ret += f"{c}"
        if idx != len(choices) - 1:
            to_ret += "|"
    to_ret += "}"
    return to_ret
