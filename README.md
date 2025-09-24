# MAS665 Assignment 2 — Nanda Adapter Integration

This repo wraps my **MAS665 Learning Buddy agent** (from Assignment 1) with the [Nanda Adapter](https://github.com/projnanda/adapter).  
The adapter makes my agent persistent, discoverable, and able to communicate with other agents on the **Agentic Web** via the **Nanda Registry**.

---

## 📖 What the Agent Does
The agent acts as a **“Data Science Learning Buddy”**. It can:
- Introduce itself and my background.
- Review or summarize a topic with concise study notes.
- Draft short professional messages.
- Quiz me or generate flashcards.
- Save outputs to Markdown for later review.

It was built using **CrewAI** and tools such as a file writer, web search, and scraping utilities.

---

## ⚙️ Setup Instructions

### 1. Clone this repo
```bash
git clone git@github.com:evenli01/mas665-assignment2-nanda-adapter.git
cd mas665-assignment2-nanda-adapter
```

### 2. Create a virtual environment (Python 3.11+)
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 3. Export environment variables
```bash
export DOMAIN_NAME="agentcoachteam.com"     # or your subdomain
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxx" # from Anthropic console
```

### 4. Ensure SSL certs are in place
Obtain certificates with Let’s Encrypt (`certbot`) and copy them here as:
```
fullchain.pem
privkey.pem
```

### 5. Run the adapter wrapper
```bash
python3 serve_my_agent.py
```

The adapter will:
- Launch a secure HTTPS server bound to your domain.
- Register the agent in the Nanda Registry.
- Enable discovery & messaging in the chat portal.

---

## 📸 Screenshot
See [`assets/nanda_registry_screenshot.png`](assets/nanda_registry_screenshot.png) for proof that the agent is registered and visible in the Nanda Registry chat portal.

---

## 📝 Feedback on the Adapter
- **Setup:** Needed Python 3.11 (Python 3.9 caused dependency errors).  
- **Certbot on Amazon Linux 2023:** Snap wasn’t available; had to install `certbot` via `dnf`/`pip`.  
- **Registry registration:** Logs were clear when the agent registered successfully.  
- **Overall:** Once configured, the adapter worked smoothly and allowed A2A messaging. Would love even easier setup scripts for AWS.

---
