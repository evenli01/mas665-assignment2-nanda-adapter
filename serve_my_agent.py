from nanda_adapter import NANDA
import os
from main import run_once   # import your MAS665 agent runner

def my_agent_logic(message: str) -> str:
    try:
        return run_once(message)
    except Exception as e:
        return f"[MAS665 Agent Error] {e}"

if __name__ == "__main__":
    nanda = NANDA(my_agent_logic)
    nanda.start_server_api(
        os.getenv("ANTHROPIC_API_KEY"),
        os.getenv("DOMAIN_NAME")
    )
