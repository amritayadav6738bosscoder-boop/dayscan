# DayScan 👻

DayScan is a small daily-task planner with a local open-weight AI helper. Its “ghost in the machine” is the task you almost forgot: add your tasks, mark them done, and ask the assistant to suggest a practical next step.

## Current features
- Add, complete, and delete daily tasks.
- Task list is saved in your browser's local storage.
- Ask a locally running Gemma model to summarize tasks and suggest a next action.
- The AI request is sent to your local Ollama service; task data is not intentionally sent to a hosted AI API.

## Requirements
- Python 3.10+
- Ollama installed and running
- A Gemma model downloaded in Ollama (the example below uses `gemma3:1b`)

## Run locally

1. Download/install Ollama from https://ollama.com.
2. Pull the model:

   ```bash
   ollama pull gemma3:1b
   ```

3. In this repository, create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   # macOS/Linux
   source .venv/bin/activate
   # Windows PowerShell: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

4. Start DayScan:

   ```bash
   python app.py
   ```

5. Open http://127.0.0.1:5000 in your browser.

Make sure Ollama is running locally before selecting **Ask local AI**. If the model is unavailable, the app shows an error rather than pretending an AI answer was generated.

## How the open AI fits
DayScan calls Ollama's local HTTP API and defaults to Gemma 3 1B. You can select another model by setting the `OLLAMA_MODEL` environment variable, provided that model is already installed in Ollama. Local inference makes it possible to keep task prompts on your own machine, subject to your local setup and the model/runtime you choose.

## Project status and limitations
This is a minimal working starter, not a background reminder service. Tasks are stored in this browser only; there is no account sync, server database, mobile notification scheduling, or independent verification of model output. Review AI suggestions before acting on them.

## Tech stack
- Python + Flask
- HTML, CSS, and vanilla JavaScript
- Ollama + Gemma (local inference)

## License
See [LICENSE](LICENSE).
