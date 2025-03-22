from typing import List, Dict, Any
from task_planner import plan_tasks
from code_executor import run_code
from memory_manager import save_log

class AgentOrchestrator:
    def __init__(self):
        self.task_planner = TaskPlanner()
        self.code_executor = CodeExecutor()
        self.memory_manager = MemoryManager()
    
    def execute_goal(self, goal: str) -> Dict[str, Any]:
        """Main entry point for executing a goal."""
        # Store the goal in memory
        self.memory_manager.store_goal(goal)
        
        # Break down goal into tasks
        tasks = self.task_planner.break_down_goal(goal)
        
        results = []
        for task in tasks:
            # Execute each task
            result = self.code_executor.execute_task(task)
            results.append(result)
            
            # Store task execution in memory
            self.memory_manager.store_task_execution(task, result)
        
        # Reflect and optimize
        self.memory_manager.reflect_and_optimize()
        
        return {
            "goal": goal,
            "tasks": tasks,
            "results": results
        }

def execute_goal(goal: str):
    """Execute a goal by breaking it into tasks and running them."""
    tasks = plan_tasks(goal)
    for task in tasks:
        code = generate_code(task["description"])
        output = run_code(code)
        save_log(task, output)

if __name__ == "__main__":
    goal = "Build a database of top Twitter creators in AI and startups, ranked by engagement."
    execute_goal(goal) 