import os
import subprocess
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_prompt(prompt_file: str) -> str:
    """Load prompt from prompts directory."""
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", prompt_file)
    with open(prompt_path, "r") as f:
        return f.read()

def generate_code(task_description: str) -> str:
    """Generate Python code for a task using GPT-4."""
    prompt = load_prompt("execution_prompt.txt").format(task=task_description)
    
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a code generation AI that writes safe, efficient Python code."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content

def run_code(code: str) -> dict:
    """Execute Python code in a sandboxed environment."""
    sandbox_dir = Path("sandbox")
    sandbox_dir.mkdir(exist_ok=True)
    
    # Create a temporary Python file
    task_file = sandbox_dir / "task.py"
    with open(task_file, "w") as f:
        f.write(code)
    
    try:
        # Execute the code in a sandboxed environment
        result = subprocess.run(
            ["python", str(task_file)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }
    finally:
        # Clean up
        if task_file.exists():
            task_file.unlink() 