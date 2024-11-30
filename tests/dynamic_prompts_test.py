import unittest
import random
from lmpc.dataclasses.prompts.dynamic_prompts import DynamicGenerativePrompt
from dynamicprompts.generators import RandomPromptGenerator
from dynamicprompts.wildcards.wildcard_manager import WildcardManager
from pathlib import Path

class TestDynamicGenerativePrompt(unittest.TestCase):
    
    def setUp(self):
        self.dynamic_persona = "I love {red|green|blue} roses"
        self.dynamic_instruction = "Please {run|walk|jump} to the store"
        self.dynamic_examples = ["Example {one|two|three}", "Sample {alpha|beta|gamma}"]
        
        self.wildcard_dir = Path("/path/to/wildcards")
        self.wildcard_manager = WildcardManager(self.wildcard_dir)
        self.random_prompt_generator = RandomPromptGenerator(self.wildcard_manager)
        
        self.prompt = DynamicGenerativePrompt(
            dynamic_persona=self.dynamic_persona,
            dynamic_instruction=self.dynamic_instruction,
            dynamic_examples=self.dynamic_examples,
            random_prompt_generator=self.random_prompt_generator
        )
        
        random.seed(42)  # Set a fixed seed for reproducibility
    
    def test_persona(self):
        persona = self.prompt.persona
        self.assertIn(persona, ["I love red roses", "I love green roses", "I love blue roses"])
    
    def test_instruction(self):
        instruction = self.prompt.instruction
        self.assertIn(instruction, ["Please run to the store", "Please walk to the store", "Please jump to the store"])
    
    def test_examples(self):
        examples = self.prompt.examples
        expected_examples = [
            ["Example one", "Example two", "Example three"],
            ["Sample alpha", "Sample beta", "Sample gamma"]
        ]
        for gen_ex, expected in zip(examples, expected_examples):
            self.assertIn(gen_ex, expected)

if __name__ == '__main__':
    unittest.main()