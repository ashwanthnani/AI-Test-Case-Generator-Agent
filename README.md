# AI Test Case Generator Agent

A Streamlit app that converts plain-English requirements into manual test cases using a local Ollama model.

## Windows setup
1. Install Python 3.10+ and Ollama.
2. Open Command Prompt in this project folder.
3. Run:

```cmd
py -m venv .venv
.venv\\Scripts\\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
ollama pull llama3.2:3b
python -m streamlit run app.py
```

If Ollama is not running, open another terminal and run `ollama serve`.
Open the local URL shown by Streamlit, usually http://localhost:8501.

The app saves history in a local SQLite database and exports CSV files. Review AI-generated cases before real QA use. This app does not test a live software product.
