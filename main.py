#!/usr/bin/env python3
"""
MAS665 - Data Science Learning Buddy (CrewAI)

Modes supported from a single prompt:
- "introduce myself"
- "explain my background in 3 sentences"
- "review <topic>"            -> concise study notes + 3 quick checks
- "summarize <topic>"         -> bullet summary + caveats + next steps
- "draft <short message>"     -> short, professional note (120–180 words)
- "quiz me on <topic>"        -> 5 concept checks w/ brief solutions
- "make flashcards for <topic>" -> 8 Q/A pairs (Anki-friendly)

Artifacts are saved in outputs/run_<timestamp>.md
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process
from crewai_tools import FileWriterTool, SerperDevTool, ScrapeWebsiteTool

# ── Environment setup ──────────────────────────────────────────────────────────
load_dotenv()  # reads .env if present
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "").strip()
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is required. Put it in .env or export it in your shell."
    )

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY  # CrewAI reads from env

# ── Tools ──────────────────────────────────────────────────────────────────────
# Always save outputs; optionally enable web search/scrape if SERPER key exists.
tools = [FileWriterTool(root_dir="outputs")]
if SERPER_API_KEY:
    os.environ["SERPER_API_KEY"] = SERPER_API_KEY
    tools.extend([SerperDevTool(), ScrapeWebsiteTool()])

# ── Persona (tailored to you) ──────────────────────────────────────────────────
PERSONA = """
You are my MAS665 "Data Science Learning Buddy" — a calm, pragmatic, and
privacy-minded study partner. You value clarity, reproducibility, and small,
iterative improvements. You can switch tone between
(1) crisp academic and (2) approachable peer.
You know about: sequential models (RNN/GRU/LSTM/PRU, BiRNN), basic ML, evaluation,
and practical study tactics. You prefer short, structured outputs with concrete next steps.
"""

buddy = Agent(
    role="MAS665 Data Science Learning Buddy",
    goal=(
        "Help me learn efficiently: explain concepts crisply, organize notes, "
        "draft short updates, quiz me, and save artifacts for later review."
    ),
    backstory=PERSONA,
    allow_delegation=False,
    verbose=True,
    tools=tools,
    llm=OPENAI_MODEL,  # model name string is supported by CrewAI
)

# ── Task builder ───────────────────────────────────────────────────────────────
def build_task(user_prompt: str) -> Task:
    ts = time.strftime("%Y%m%d_%H%M%S")
    outfile = f"outputs/run_{ts}.md"

    description = f"""
You are the MAS665 Data Science Learning Buddy.

USER PROMPT:
{user_prompt}

OPERATING MODES (detect from the prompt and do ONE):
1) "introduce yourself" / "introduce yourself to the class":
   - 5–7 sentences, friendly but concise. Include how you assist with MAS665.

2) "explain my background in 3 sentences":
   - Exactly 3 crisp sentences from the perspective of a motivated MAS665 student
     with interests in data privacy, device reliability, and explainable ML.

3) "review <topic>":
   - Create focused study notes in sections:
     * Key Ideas (bullets)
     * Minimal Math (clear equations or definitions if relevant)
     * Common Pitfalls
     * Quick Checks (3 short questions with answers)

4) "summarize <topic>":
   - Bullet summary (6–10 bullets), "Caveats", "What To Practice Next".

5) "draft <short message>":
   - Write a professional message (120–180 words) for the described context
     (e.g., email/slack/class post). Clear, polite, no fluff.

6) "quiz me on <topic>":
   - 5 concept checks. Format each as:
     Q) ...
     A) (2–4 lines, correct but brief)

7) "make flashcards for <topic>":
   - 8 Q/A pairs; keep each answer ≤3 lines. Prefix with 'Flashcard 1:' etc.

ALWAYS:
- End with a section "Next steps" containing exactly 3 actionable bullets.
- Save the FULL response to '{outfile}' using the file writer tool.
- If web tools are available and the prompt implies current events or definitions that might drift,
  you MAY use search/scrape to verify terminology; otherwise rely on core knowledge.
"""
    expected_output = f"""
A well-structured Markdown response aligned to the detected mode, saved as {outfile}.
Includes a final "Next steps" with exactly 3 bullets.
"""
    return Task(description=description, expected_output=expected_output, agent=buddy)

# ── Runner ─────────────────────────────────────────────────────────────────────
def run_once(user_prompt: str) -> str:
    task = build_task(user_prompt)
    crew = Crew(
        agents=[buddy],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )
    result = crew.kickoff()
    print("\n──────── OUTPUT (preview) ────────")
    print(result)
    print("──────────────────────────────────")
    return result

if __name__ == "__main__":
    Path("outputs").mkdir(parents=True, exist_ok=True)
    print("📘 MAS665 — Data Science Learning Buddy")
    prompt = input("Enter a prompt (e.g., 'introduce yourself to the class'): ").strip()
    if not prompt:
        prompt = "introduce yourself to the class"
        print(f"Using default: {prompt}")
    run_once(prompt)
