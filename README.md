# Code-to-Venture

This project uses a crew of AI agents, powered by the `crewAI` framework, to automatically analyze a local software project and generate potential business use cases for it.

The system intelligently scans a project directory, understands its technical implementation, and then brainstorms creative, market-focused business strategies based on its findings.

## 🚀 Key Features

* **Automated Codebase Analysis**: Automatically reads and understands the purpose of a project from its source code.
* **Intelligent File Filtering**: A custom tool programmatically ignores irrelevant files and directories (like `.venv`, `node_modules`, `.git`, `__pycache__`) to focus only on what matters.
* **Multi-Agent System**: Utilizes a two-agent crew for specialized tasks:
    * **👨‍💻 Code Analyst Agent**: Analyzes the technical aspects of the code.
    * **📈 Business Strategist Agent**: Brainstorms business models based on the technical analysis.
* **Dynamic Use Case Generation**: Produces a structured report with multiple business ideas, including target audience, value proposition, and monetization strategies.
* **Extensible & Customizable**: Easily adapt the agents, tasks, or tools to fit different needs or use different Large Language Models (LLMs).

## ⚙️ How It Works

The project operates through a sequential `crewAI` process:

1.  **Input**: The user provides a local path to a project directory.
2.  **File Filtering**: The custom `FilteredDirectoryReadTool` scans the directory, ignoring predefined unnecessary files and folders, and returns a clean list of relevant file paths.
3.  **Task 1: Code Analysis**:
    * The **Code Analyst Agent** receives the list of relevant files.
    * It uses the `FileReadTool` to read the content of the most important files (e.g., `README.md`, `requirements.txt`, key source code files).
    * It produces a technical summary detailing the project's purpose, technology stack, and core features.
4.  **Task 2: Business Strategy**:
    * The **Business Strategist Agent** takes the technical summary from the first task as its context.
    * It brainstorms and formulates several business use cases based on the project's capabilities.
5.  **Output**: The crew provides a final, consolidated report containing both the technical summary and the detailed business use cases.

## 📋 Prerequisites

* Python 3.8+
* An API key from an LLM provider (e.g., [Groq](https://console.groq.com/keys), OpenAI, Anthropic, Google).

## 🛠️ Installation & Setup

**1. Clone the Repository**
```bash
git clone <your-repository-url>
cd <repository-name>
```
**2. Create a Virtual Environment**

It's highly recommended to use a virtual environment to manage dependencies.

- On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
- On Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

**3.Install Dependencies**

Create a file named `requirements.txt` with the following content:

```
crewai==0.35.8
crewai-tools==0.4.2
langchain-groq==0.1.5
# Or if you prefer OpenAI:
# langchain-openai==0.1.8
```

Then, install the packages:
```bash
pip install -r requirements.txt
```

**4.Configure Your API Key**

Open the `main.py` file and find the "Setup API Keys" section. Uncomment the relevant lines for your chosen LLM provider and paste your API key.

```python
import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY_HERE"
llm = ChatGroq(model="<MODEL_NAME>", temperature=0.7)
```
## ▶️ How to Run
Execute the script from your terminal:

```bash
python main.py
```

The script will then prompt you to enter the path to the project you want to analyze:

```bash
## Welcome to the Business Use Case Generator Crew! ##
Please enter the full path to your project directory: /Users/yourname/Documents/projects/my-cool-app
```

The crew will start its analysis, and you will see the agents' progress printed to the console. The final report will be displayed at the end.

## 🔧 Customization
You can easily customize this project for your own needs.

- **Change the LLM:** In `main.py`, you can swap `OPENAI` with any other LangChain-compatible model, such as `ChatGroq` or `ChatAnthropic` or `Gemini`. Just make sure to install the required library (pip install langchain-openai) and set the correct environment variable (OPENAI_API_KEY).

- **Modify Agent Roles:** You can change the `role`, `goal`, and `backstory` for each agent to alter its personality and focus. For example, you could change the "Business Strategist" to a "Marketing Specialist" to get ideas for go-to-market strategies instead.

- **Adjust the File Filter:** To ignore more file types or directories, simply add them to the `ignore_patterns` or `ignore_files` lists inside the `FilteredDirectoryReadTool` class in main.py.

## 📜 License
This project is licensed under the MIT License. See the LICENSE file for more details.