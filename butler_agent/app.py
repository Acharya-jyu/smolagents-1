import yaml
import os
from smolagents import GradioUI, CodeAgent, LiteLLMModel

# Get current directory path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

from tools.suggest_menu import SimpleTool as SuggestMenu
from tools.web_search import DuckDuckGoSearchTool as WebSearch
from tools.visit_webpage import VisitWebpageTool as VisitWebpage
from tools.final_answer import FinalAnswerTool as FinalAnswer

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

model = LiteLLMModel(
model_id='gemini/gemini-2.0-flash',
api_key=GOOGLE_API_KEY
api_base=None,
)

suggest_menu = SuggestMenu()
web_search = WebSearch()
visit_webpage = VisitWebpage()
final_answer = FinalAnswer()


with open(os.path.join(CURRENT_DIR, "prompts.yaml"), 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

agent = CodeAgent(
    model=model,
    tools=[suggest_menu, web_search, visit_webpage],
    managed_agents=[],
    max_steps=20,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    executor_type='local',
    executor_kwargs={},
    max_print_outputs_length=None,
    prompt_templates=prompt_templates
)
if __name__ == "__main__":
    GradioUI(agent).launch()
