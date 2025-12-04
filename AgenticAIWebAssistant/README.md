Agentic AI Web Assistant - refactored
------------------------------------

Structure:
- utils/: runtime/symbol helpers
- tools/: finance, chart, calculator
- AgentExecutor.py: agent + tools + executor
- cli_main.py: CLI runner
- ui_main.py: Streamlit UI runner

Run CLI:
    python cli_main.py

Run Streamlit UI:
    streamlit run ui_main.py
