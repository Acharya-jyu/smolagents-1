from smolagents import Tool
from typing import Any, Optional

class SimpleTool(Tool):
    name = "suggest_menu"
    description = "Suggests a menu based on the occasion."
    inputs = {'occasion': {'type': 'string', 'description': 'The type of occasion for the party. Allowed values are: - "casual": Menu for casual party. - "formal": Menu for formal party. - "superhero": Menu for superhero party. - "custom": Custom menu.'}}
    output_type = "string"

    def forward(self, occasion: str) -> str:
        """
        Suggests a menu based on the occasion.
        Args:
            occasion (str): The type of occasion for the party. Allowed values are:
                            - "casual": Menu for casual party.
                            - "formal": Menu for formal party.
                            - "superhero": Menu for superhero party.
                            - "custom": Custom menu.
        """
        if occasion == "casual":
            return "Pizza, snacks, and drinks."
        elif occasion == "formal":
            return "3-course dinner with wine and dessert."
        elif occasion == "superhero":
            return "Buffet with high-energy and healthy food."
        else:
            return "Custom menu for the butler."