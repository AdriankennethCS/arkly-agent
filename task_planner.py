import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_prompt(prompt_file: str) -> str:
    """Load prompt from prompts directory."""
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", prompt_file)
    with open(prompt_path, "r") as f:
        return f.read()

def plan_tasks(goal: str) -> list:
    """Break down a goal into executable tasks."""
    prompt = load_prompt("task_prompt.txt").format(goal=goal)
    
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a task planning AI that breaks down goals into executable tasks."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    try:
        tasks = json.loads(response.choices[0].message.content)
        return tasks
    except json.JSONDecodeError:
        return [{
            "id": "task_1",
            "description": f"Error parsing tasks for goal: {goal}",
            "dependencies": []
        }] 