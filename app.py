# This is the first draft of the tutorial.
from huggingface_hub import login
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, tool, LiteLLMModel
import numpy as np
import time
import datetime
import os
os.environ["PYTHONUTF8"] = "1"   
# Do not hardcode tokens in the code
HF_TOKEN = os.environ.get("HF_TOKEN")  # Get from environment
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")  # Get from environment

login(token=HF_TOKEN)

# Initialize the agent with the DuckDuckGo search tool and a Hugging Face model
# Use a smaller model that can run locally
model = LiteLLMModel(
    model_id="gemini/gemini-2.0-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)

# model=HfApiModel(model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud/')

agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model, add_base_tools=True)
agent.run("Search for the best music recommendations for a party at the Wayne's mansion.")

# Tool to suggest a menu based on the occasion
@tool
def suggest_menu(occasion: str) -> str:
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

# Loading a custom tool to our agent
# The tool is used to suggest a menu based on the occasion.
agent = CodeAgent(tools=[suggest_menu], model=model, add_base_tools=True)
agent.run("Prepare a formal menu for the party.")

# The agent will calculate the time needed for the party preparation.
agent = CodeAgent(tools=[suggest_menu,DuckDuckGoSearchTool()], model=model, add_base_tools=True, additional_authorized_imports=['datetime'])
agent.run(
    """
    Alfred needs to prepare for the party. Here are the tasks:
    1. Prepare the drinks - 30 minutes
    2. Decorate the mansion - 60 minutes
    3. Set up the menu - 45 minutes
    4. Prepare the music and playlist - 45 minutes

    If we start right now, at what time will the party be ready?
    """
)
 
agent.push_to_hub('acharya-jyu/SampleSmolagent-1', commit_message='First commit')