import unittest
from pathlib import Path
from lmpc.dataclasses.character import Character, Alignment, Opinion


class TestCharacter(unittest.TestCase):

    def setUp(self):
        self.character = Character(
            name="John Doe",
            origin_story="Once upon a time...",
            alignment=Alignment.NEUTRAL_GOOD,
            values=["Honesty", "Bravery"],
            objectives=["Save the world", "Find the treasure"],
            opinions=[
                Opinion(title="Opinion 1", content="Content 1"),
                Opinion(title="Opinion 2", content="Content 2"),
            ],
        )
        self.file_path = Path("test_character.md")

    def tearDown(self):
        if self.file_path.exists():
            self.file_path.unlink()

    def test_save_to_markdown(self):
        self.character.save_to_markdown(self.file_path)
        content = self.file_path.read_text()

        expected_content = (
            "# John Doe\n"
            "## Backstory\nOnce upon a time...\n"
            "## Alignment\nNeutral Good\n"
            "## Values\n"
            "- Honesty\n"
            "- Bravery\n"
            "## Objectives\n"
            "- Save the world\n"
            "- Find the treasure\n"
            "## Opinions\n"
            "### Opinion 1\nContent 1\n"
            "### Opinion 2\nContent 2\n"
        )

        self.assertEqual(content, expected_content)


if __name__ == "__main__":
    unittest.main()
