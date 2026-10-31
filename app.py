import os
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma3:1b")


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/suggest")
def suggest():
    payload = request.get_json(silent=True) or {}
    tasks = payload.get("tasks", [])

    if not isinstance(tasks, list) or len(tasks) > 100:
        return jsonify({"error": "Please send a task list with at most 100 items."}), 400

    clean_tasks = []
    for task in tasks:
        if isinstance(task, str):
            task = task.strip()
            if task:
                clean_tasks.append(task[:300])

    if not clean_tasks:
        return jsonify({"error": "Add at least one task before asking the AI."}), 400

    prompt = (
        "You are DayScan, a calm and practical daily planning assistant. "
        "Use only the task list below. Do not claim you completed tasks. "
        "Give a short summary and recommend one manageable next action. "
        "Be supportive, not judgmental. If priorities are unclear, say so.\n\n"
        "Today's tasks:\n- " + "\n- ".join(clean_tasks) +
        "\n\nRespond in plain text, under 120 words."
    )

    try:
        response = requests.post(
            f"{OLLAMA_URL.rstrip('/')}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=90,
        )
        response.raise_for_status()
        result = response.json().get("response", "").strip()
        if not result:
            return jsonify({"error": "The local model returned an empty response."}), 502
        return jsonify({"suggestion": result, "model": OLLAMA_MODEL})
    except requests.RequestException:
        return jsonify({
            "error": (
                "Could not reach Ollama. Start Ollama and run "
                f"'ollama pull {OLLAMA_MODEL}', then try again."
            )
        }), 503
    except ValueError:
        return jsonify({"error": "Ollama returned an unreadable response."}), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
