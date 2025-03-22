from flask import Flask, request, jsonify
from agent_orchestrator import AgentOrchestrator

app = Flask(__name__)
orchestrator = AgentOrchestrator()

@app.route("/execute", methods=["POST"])
def execute_goal():
    """Execute a goal through the web interface."""
    data = request.get_json()
    if not data or "goal" not in data:
        return jsonify({"error": "No goal provided"}), 400
    
    try:
        result = orchestrator.execute_goal(data["goal"])
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True) 