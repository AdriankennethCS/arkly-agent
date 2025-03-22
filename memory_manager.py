from typing import Dict, Any, List
import json
from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MemoryManager:
    def __init__(self):
        self.memory_dir = Path("memory")
        self.memory_dir.mkdir(exist_ok=True)
        self.reflection_prompt = self._load_prompt("reflection_prompt.txt")
    
    def _load_prompt(self, prompt_file: str) -> str:
        """Load prompt from prompts directory."""
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", prompt_file)
        with open(prompt_path, "r") as f:
            return f.read()
    
    def store_goal(self, goal: str):
        """Store a new goal in memory."""
        goals_file = self.memory_dir / "goals.json"
        goals = self._load_json(goals_file, [])
        goals.append({
            "goal": goal,
            "timestamp": str(Path.timestamp())
        })
        self._save_json(goals_file, goals)
    
    def store_task_execution(self, task: Dict[str, str], result: Dict[str, Any]):
        """Store task execution results in memory."""
        executions_file = self.memory_dir / "executions.json"
        executions = self._load_json(executions_file, [])
        executions.append({
            "task": task,
            "result": result,
            "timestamp": str(Path.timestamp())
        })
        self._save_json(executions_file, executions)
    
    def reflect_and_optimize(self):
        """Analyze past executions and optimize future task planning."""
        # TODO: Implement actual reflection and optimization logic
        pass
    
    def _load_json(self, file_path: Path, default: Any) -> Any:
        """Load JSON from file or return default if file doesn't exist."""
        if file_path.exists():
            with open(file_path, "r") as f:
                return json.load(f)
        return default
    
    def _save_json(self, file_path: Path, data: Any):
        """Save data as JSON to file."""
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

def save_log(task: dict, output: dict):
    """Save task execution results and analyze them."""
    memory_dir = Path("memory")
    memory_dir.mkdir(exist_ok=True)
    
    # Save raw execution log
    executions_file = memory_dir / "executions.json"
    executions = load_json(executions_file, [])
    executions.append({
        "task": task,
        "output": output,
        "timestamp": str(Path.timestamp())
    })
    save_json(executions_file, executions)
    
    # Analyze execution
    analysis = analyze_execution(task, output)
    
    # Save analysis
    analysis_file = memory_dir / "analysis.json"
    analyses = load_json(analysis_file, [])
    analyses.append(analysis)
    save_json(analysis_file, analyses)

def analyze_execution(task: dict, output: dict) -> dict:
    """Analyze task execution using GPT-4."""
    prompt = load_prompt("reflection_prompt.txt").format(
        task=json.dumps(task),
        output=json.dumps(output),
        error=output.get("error", "")
    )
    
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are an analysis AI that reviews task executions and suggests improvements."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        return {
            "status": "error",
            "analysis": {
                "root_cause": "Failed to parse analysis",
                "fixes": ["Check JSON formatting"],
                "prevention": ["Validate JSON response"]
            },
            "learnings": [],
            "metrics": {
                "performance": "unknown",
                "efficiency": "unknown"
            },
            "next_steps": {
                "immediate": ["Fix JSON parsing"],
                "long_term": ["Improve error handling"],
                "system": ["Add response validation"]
            }
        }

def load_json(file_path: Path, default: any) -> any:
    """Load JSON from file or return default if file doesn't exist."""
    if file_path.exists():
        with open(file_path, "r") as f:
            return json.load(f)
    return default

def save_json(file_path: Path, data: any):
    """Save data as JSON to file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2) 