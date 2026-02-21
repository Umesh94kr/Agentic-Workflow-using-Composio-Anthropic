# Agentic Workflow using Composio + Anthropic

Build an agentic workflow that connects external tools via **Composio** and uses **Anthropic LLM** for reasoning and orchestration.

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv myenv
source myenv/bin/activate
```

### 3️⃣ Create & Activate Virtual Environment
```bash 
pip install -r requirements.txt
```

🔐 Environment Configuration

Create a .env file in the root directory and add:

```
COMPOSIO_API_KEY=YOUR_COMPOSIO_API_KEY
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY
```
🔑 How to Get API Keys

Composio API Key
Create an account at: https://composio.dev/

Generate your API key from the dashboard.

Anthropic API Key
Create an account at: https://console.anthropic.com/

Generate your API key from the API settings section.

🛠 Tool Configuration (Composio)

 - Visit the Composio dashboard.
 - Explore available toolkits.
 - Enable and configure tools you want to use (e.g., gmail, notion, etc.).
 - Ensure proper authentication is completed for each tool.

And also I had used Ollama to run reward agent (for evaluation)
you can change LLM in reward.py otherwise first take a pull of `llama3.2`

Check my second readme in this repo : Setup_for_local_ollama3.2.md

▶️ Run the Application
```
bash
python main.py
```

🧠 What Happens Next?

- The program prompts for a user_id.
- You choose the tool you want to connect.
- If the tool is not authenticated:

    > A secure authentication link will be generated.
    > Complete authentication in your browser.

- Once authenticated, the agent executes tasks using:
    > Composio for tool actions
    > Anthropic LLM for reasoning & decision-making

Follow the prompts and interact with your agent.


Thank You ❤️