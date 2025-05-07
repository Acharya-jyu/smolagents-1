# This is the second draft of the tutorial.
from huggingface_hub import login, upload_folder
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, tool, LiteLLMModel
import numpy as np
import time
import datetime
import os, sys
import shutil

# Set UTF-8 as default encoding
os.environ["PYTHONUTF8"] = "1"
 
# Do not hardcode tokens in the code
HF_TOKEN = os.environ.get("HF_TOKEN")  # Get from environment
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")  # Get from environment

# Login to Hugging Face
login(token=HF_TOKEN)

# Initialize the model
model = LiteLLMModel(
    model_id="gemini/gemini-2.0-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)

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

# Create the agent
agent = CodeAgent(
    tools=[suggest_menu, DuckDuckGoSearchTool()], 
    model=model, 
    add_base_tools=True, 
    additional_authorized_imports=['datetime']
)

try:
    # Step 1: Save the agent locally to a folder
    temp_folder = "./butler_agent"
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)  # Remove folder if it exists
    
    print("Saving agent locally...")
    agent.save(temp_folder)
    
    # Step 2: Create a README.md file
    readme_content = """# Butler Menu Agent

This agent helps suggest menus for different types of parties and occasions.

## Features
- Menu suggestions based on occasion type
- Web search capabilities 
- Support for different party types

## How to Use
1. Ask the agent for menu suggestions for different types of parties
2. Get customized menu recommendations

Created with smolagents.
"""
    
    with open(os.path.join(temp_folder, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Step 3: Use huggingface_hub to upload the folder
    repo_id = "acharya-jyu/SampleSmolagents-1"
    print(f"Pushing agent to {repo_id}...")
    
    result = upload_folder(
        folder_path=temp_folder,
        repo_id=repo_id,
        repo_type="space",
        token=HF_TOKEN,
        commit_message="Initial commit for Butler Menu Agent"
    )
    
    print("Upload successful!")
    print(f"Agent available at: https://huggingface.co/spaces/{repo_id}")
    
except Exception as e:
    print(f"Error during push: {e}")
    import traceback
    traceback.print_exc()