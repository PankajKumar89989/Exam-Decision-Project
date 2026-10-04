# AI Study Decision Engine

A beginner-friendly Python + Streamlit project that suggests a next study action based on available time, exam proximity, topics remaining, difficulty, and energy level.

## Features
- Interactive Streamlit form and decision summary
- Local rule-based demo mode that works without an API key
- Optional Laya API integration via environment variables
- Input-aware recommendation explanations and urgency level
- Error handling and unit tests

> The local mode is a transparent rule-based demonstration, not a trained machine-learning model. The Laya API mode depends on valid credentials, internet access, account access, and the provider's current API contract.

## Requirements
- Python 3.10 or newer
- VS Code
- Internet connection for installing packages; also required for Laya API mode

## Run in VS Code (Windows)

1. Extract the ZIP to a folder you can find, for example `Documents\AI-Study-Decision-Engine`.
2. Open VS Code, choose **File → Open Folder**, and select that extracted folder.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

5. Activate it in PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt terminal instead and run:

   ```bat
   .venv\Scripts\activate.bat
   ```

6. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

7. In VS Code, choose the interpreter inside `.venv` if prompted (**Ctrl+Shift+P → Python: Select Interpreter**).
8. Start the app:

   ```powershell
   python -m streamlit run app.py
   ```

9. Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser. Local demo mode works without a Laya key; leave the API checkbox unchecked.

## Optional: enable Laya API

1. Copy `.env.example` to a new file named `.env` in the project root.
2. Replace the placeholder with your own valid API key and confirm the endpoint/API schema with Laya's current documentation.
3. Keep `.env` private. It is listed in `.gitignore`; never paste API keys into source code or commit them to GitHub.
4. Tick **Use Laya API** in the app to try API mode. If the provider's API contract or account requirements have changed, update `laya_client.py` accordingly.

## Run tests

```powershell
python -m pytest -q
```

## Upload to GitHub

1. Create a new empty repository on GitHub, e.g. `ai-study-decision-engine`. Do not upload `.env` or your `.venv` folder.
2. In the VS Code terminal, from this project's root folder, run:

   ```powershell
   git init
   git add .
   git status
   git commit -m "Build AI Study Decision Engine"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/ai-study-decision-engine.git
   git push -u origin main
   ```

3. Replace `YOUR-USERNAME` with your GitHub username. If Git asks you to authenticate, use GitHub's sign-in flow or a supported credential manager; your GitHub password is not used as a Git HTTPS password.
4. Check the repository page and make sure `README.md`, Python files, `requirements.txt`, and tests are present. Confirm `.env` is absent.

If `git remote add origin` says a remote already exists, run `git remote -v` and update it with `git remote set-url origin https://github.com/YOUR-USERNAME/ai-study-decision-engine.git`.

## Project structure

```text
AI-Study-Decision-Engine/
├── app.py
├── decision_engine.py
├── laya_client.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── tests/
    └── test_decision_engine.py
```

## Suggested portfolio improvements
- Add saved study plans and a history page
- Add subject-wise targets and revision scheduling
- Add accessibility and mobile layout checks
- Document limitations and test the API integration with mocked responses
