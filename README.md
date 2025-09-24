# MAS665 Assignment 2 — Nanda Adapter Integration

This repo wraps my **MAS665 Learning Buddy agent** (from Assignment 1) with the [Nanda Adapter](https://github.com/projnanda/adapter).
The adapter makes the agent persistent, network-addressable, and able to participate in A2A (agent-to-agent) messaging via the **Nanda Registry**.

---

## ✅ Deliverables Checklist

- **GitHub repo with code, configuration, and adapter integration:** ✔️ (this repo)
- **Screenshot of agent registered and visible on the Nanda Registry chat platform:**  
  - ⚠️ *Pending due to Registry access issue.* The Nanda Registry account sign‑in / programmatic registration endpoint is currently failing on my account, so I cannot obtain the in‑portal screenshot yet. See **Registry Status & Evidence** below and `myagent.out` for proof that the agent is running and exposing endpoints. A placeholder is included: `assets/nanda_registry_screenshot.png`.
- **Short note explaining what the agent does + feedback:** ✔️ See **What the Agent Does** and **Feedback**.

---

## 📖 What the Agent Does

**Role:** *Data Science Learning Buddy*

**Capabilities:**
- Introduce itself and my background.
- Summarize topics into concise study notes.
- Draft short professional emails/messages.
- Quiz me / generate flashcards.
- Save outputs to Markdown for later review.

**Tech:** CrewAI-based agent + simple tools (file write, web fetch).  
The Nanda Adapter exposes it over HTTP(S) and supports A2A via the Registry.

---

## 🟢 Registry Status & Evidence (`myagent.out`)

> The Nanda Registry has a temporary **account sign‑in / registration** issue for my account.  
> Auto-registration attempts return an error at the root registry path (POST not supported).  
> Despite this, the agent is **running**, **bridged**, and **exposes public endpoints**; a **manual assignment link** is printed in logs.

**Proof from `myagent.out` (excerpt):**
```
🤖 NANDA initialized with custom improvement logic: my_agent_logic
✅ Detected server IP: 3.134.240.151
🤖 Auto-generated agent ID: agents141376
🔗 Auto-generated public URL: http://3.134.240.151:6000
Using registry URL from file: https://chat.nanda-registry.com
Registering agent agents141376 with URL http://3.134.240.151:6000 at registry https://chat.nanda-registry.com...

🚀 Starting Agent agents141376 bridge on port 6000
Message improvement feature is ENABLED
Logging conversations to /home/ec2-user/mas665-assignment2-nanda-adapter/conversation_logs
Starting A2A server on http://0.0.0.0:6000/a2a

📡 API Endpoints:
  GET  https://agentcoachteam.com:6001/api/health
  POST https://agentcoachteam.com:6001/api/send
  GET  https://agentcoachteam.com:6001/api/agents/list
  POST https://agentcoachteam.com:6001/api/receive_message
  GET  https://agentcoachteam.com:6001/api/render

******************************************************
You can assign your agent using this link
https://chat.nanda-registry.com/landing.html?agentId=agents141376
******************************************************
```

**Interpretation:**
- Adapter initialized; public IP discovered.
- **AgentBridge** is running on **port 6000**, A2A endpoint `/a2a` is live.
- **UI HTTPS API** is up on **port 6001** (endpoints listed).
- **Manual assignment link** was produced.
- In other runs, the registry responded `HTTP 501 Unsupported method ('POST')` to the root path, indicating a method/path mismatch for programmatic registration while the agent itself remains healthy.

> Once the Registry sign‑in/API is restored, I will add the in‑portal screenshot (`assets/nanda_registry_screenshot.png`) showing the agent visible in the Registry chat.

---

## ⚙️ Setup / Run

> Requires **Python 3.11+**.

```bash
git clone git@github.com:evenli01/mas665-assignment2-nanda-adapter.git
cd mas665-assignment2-nanda-adapter

python3.11 -m venv nanda-venv
source nanda-venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### TLS Certificates
Place these files in the repo root (symlinks are fine):
```
fullchain.pem
privkey.pem
```

### Environment (examples)
```bash
export DOMAIN_NAME="agentcoachteam.com"          # or your host
# Route agent replies to your local UI receiver:
export UI_CLIENT_URL="https://localhost:6001/api/receive_message"
# Optional model keys, etc.
# export ANTHROPIC_API_KEY="sk-ant-xxxx"
```

### Start the adapter
Foreground:
```bash
python3 serve_my_agent.py
```

Background with logging:
```bash
nohup python3 serve_my_agent.py > ~/myagent.out 2>&1 &
tail -f ~/myagent.out
```

---

## 💬 Send a Test Message & View Conversation Logs

Once the servers are up, send a message to your **current agentId** (see `myagent.out`, e.g., `agents141376`):

```bash
# health
curl -k -i https://localhost:6001/api/health

# send a message
curl -k -s -X POST https://localhost:6001/api/send   -H "Content-Type: application/json"   -d '{"agentId":"agents141376","message":"Hello! Please confirm you received this test message."}'
```

**Conversation logs** are written to:
```
./conversation_logs/
```

Inspect:
```bash
ls -lt conversation_logs
tail -n 200 -f conversation_logs/*
```

Render the latest message via API:
```bash
curl -k -i https://localhost:6001/api/render
```

> If you only see **sent** messages but not **agent replies**, ensure `UI_CLIENT_URL` points to your local UI receiver:
> `export UI_CLIENT_URL="https://localhost:6001/api/receive_message"` and restart the agent.

---

## 🪛 Troubleshooting

- **Port 6001 already in use**:
  ```bash
  lsof -i :6001
  kill <PID>    # or: pkill -f run_ui_agent_https
  ```
  Then restart, or configure a different UI port if supported.

- **Registry registration (HTTP 501 Unsupported method 'POST')**:
  - The Registry root path currently rejects POST. Use the **manual assignment link** printed in logs:
    ```
    https://chat.nanda-registry.com/landing.html?agentId=<yourId>
    ```
  - Once Registry access is restored, open that link to complete assignment and capture the required screenshot.

---

## 📸 Screenshots

Add screenshots here once available:
- `assets/agent_running.png` — agent & endpoints healthy (added by me).
- `assets/registry_signin_issue.png` — evidence of the sign‑in/POST issue.
- `assets/nanda_registry_screenshot.png` — **to be added** after Registry access is restored.

---

## 📝 Feedback on the Adapter

- **Setup experience:** Smooth with Python 3.11. TLS cert placement and env vars were straightforward.
- **Observability:** Logs are clear—agentId, public URL, endpoints, and the manual assignment link are printed.
- **Registry integration:** Account sign‑in / POST-to-root behavior currently blocks programmatic registration for my account. A doc note clarifying the correct endpoint/method (or a fallback GET) would help.
- **Nice to have:** A small health page at `/` on port 6001, and a one-command installer for Amazon Linux 2023 (certs + service file).

---

## 🧹 Repo Hygiene

Runtime logs and secrets are ignored to avoid accidental commits. Suggested `.gitignore` entries:
```
logs_agents*/
conversation_logs/
myagent*.out
*.pem
```
