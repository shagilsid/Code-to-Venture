import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gemini-2.5-flash",  # Note the provider prefix
    temperature=0.5,
)

class FilteredDirectoryReadTool(BaseTool):
    name: str = "Filtered Directory Reader"
    description: str = "Reads a directory's file structure, intelligently ignoring irrelevant files and directories."

    def _run(self, directory_path: str) -> str:
        """
        Walks through a directory, filtering out specified files and folders,
        and returns a string with the paths of the relevant files.
        """
        # Define patterns to ignore for both directories and files
        ignore_patterns = [
            '.venv', '.git', '__pycache__', 'node_modules', 'build', 'dist',
            'coverage', '.idea', '.vscode', 'logs'
        ]
        ignore_files = [
            '.gitignore', '.env', 'poetry.lock', 'package-lock.json', '.DS_Store'
        ]

        relevant_files = []
        try:
            for root, dirs, files in os.walk(directory_path, topdown=True):
                # Filter out ignored directories in place
                dirs[:] = [d for d in dirs if d not in ignore_patterns]

                for file in files:
                    if file not in ignore_files:
                        full_path = os.path.join(root, file)
                        # Further check if any part of the path contains an ignore pattern
                        if not any(f"/{pattern}/" in full_path for pattern in ignore_patterns):
                             relevant_files.append(full_path)

            if not relevant_files:
                return "No relevant files found in the directory after filtering."

            return "Found the following relevant files:\n" + "\n".join(relevant_files)
        except Exception as e:
            return f"Error reading directory {directory_path}: {e}"

filtered_directory_tool = FilteredDirectoryReadTool()
file_read_tool = FileReadTool()

code_analyst_agent = Agent(
    role='Senior Code Analyst',
    goal='Analyze the provided codebase to understand its purpose, features, and tech stack.',
    backstory=(
        "You are an expert software developer with a knack for quickly understanding code. "
        "You use specialized tools to efficiently list only the important files, allowing you to focus on what truly matters."
    ),
    # The agent now uses our new custom tool
    tools=[filtered_directory_tool, file_read_tool],
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# Agent 2: Business Strategist 📈
business_strategist_agent = Agent(
    role='Business Development Strategist',
    goal='Identify and develop compelling business use cases for a given technology project.',
    backstory=(
        "You have a sharp eye for market opportunities and excel at turning technical innovations into profitable business ventures."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm
)


# --- 4. Define Tasks with Simplified Descriptions ---

# Task 1: Analyze the Project (with the new tool)
code_analysis_task = Task(
    description=(
        "Analyze the project located at the directory: '{project_path}'.\n\n"
        "Your workflow is as follows:\n"
        "1. Use the `Filtered Directory Reader` tool to get a list of all relevant files.\n"
        "2. Based on the file list, identify the most critical files for understanding the project (e.g., README, main scripts, requirements).\n"
        "3. For each of those critical files, use the `file_read_tool` to read its content.\n"
        "4. Synthesize this information into a concise technical summary."
    ),
    expected_output=(
        "A detailed technical summary including:\n"
        "1. The project's primary purpose and functionality.\n"
        "2. Key features and capabilities discovered from the source code.\n"
        "3. The technology stack (languages, frameworks, libraries).\n"
        "4. A high-level overview of the code structure."
    ),
    agent=code_analyst_agent
)

# Task 2: Brainstorm Business Use Cases
business_use_case_task = Task(
    description=(
        "Based on the technical summary of the project, brainstorm potential business use cases."
    ),
    expected_output=(
        "A well-structured report with at least three potential business use cases. Each use case should include:\n"
        "1. **Use Case Title**: A catchy name for the business idea.\n"
        "2. **Target Audience**: Specific group of users or businesses.\n"
        "3. **Value Proposition**: The unique value or problem solved for the audience.\n"
        "4. **Potential Monetization Strategy**: How to generate revenue."
    ),
    agent=business_strategist_agent,
    context=[code_analysis_task],
    output_file="business_use_cases_report.md"  # Save the output to a file
)


project_crew = Crew(
    agents=[code_analyst_agent, business_strategist_agent],
    tasks=[code_analysis_task, business_use_case_task],
    process=Process.sequential, # Tasks will be executed one after another
    verbose=True
)


if __name__ == "__main__":
    print("## Welcome to the Business Use Case Generator Crew! ##")
    project_path = input("Please enter the full path to your project directory: ")

    # Create a dictionary with the project path to kick off the crew
    inputs = {'project_path': project_path}

    print("\n\n--- Starting Crew Analysis ---")
    # Kick off the crew's work
    # Note: If you haven't set up an LLM, this will raise an error.
    # The code is structured to be ready-to-run once the LLM is configured.
    try:
        result = project_crew.kickoff(inputs=inputs)
        print("\n\n--- Crew Analysis Complete ---")
        print("Final Report:")
        print(result)
    except Exception as e:
        print(f"\nAn error occurred. Please ensure you have set up your LLM API key.")
        print(f"Error: {e}")
        print("\n--- SIMULATED OUTPUT ---")
        print("""
        **Final Report:**

        Here is a sample report based on an analysis of a hypothetical project.

        **Technical Summary:**
        1.  **Project's Purpose**: The project is a Python-based web scraping tool that extracts product information from e-commerce sites.
        2.  **Key Features**: It can scrape product titles, prices, reviews, and images. It supports multiple sites and can export data to CSV.
        3.  **Technology Stack**: Python, BeautifulSoup, Requests.
        4.  **Code Structure**: A main script to handle user input, a `scrapers` module for site-specific logic, and a `utils` module for data export.

        **Business Use Cases Report:**

        **1. Use Case Title: PricePulse Competitive Analysis**
        * **Target Audience**: E-commerce store owners and marketing managers.
        * **Value Proposition**: Provides real-time pricing and product assortment data from competitors, enabling dynamic pricing strategies and market positioning.
        * **Monetization Strategy**: Monthly Subscription (SaaS) model with different tiers based on the number of tracked products and competitors.

        **2. Use Case Title: MarketGuard Brand Protection**
        * **Target Audience**: Brands and manufacturers.
        * **Value Proposition**: Monitors online marketplaces for unauthorized sellers, counterfeit products, and Minimum Advertised Price (MAP) violations to protect brand integrity.
        * **Monetization Strategy**: Annual licensing fee per brand, with add-on services for enforcement actions.

        **3. Use Case Title: TrendScout Product Research**
        * **Target Audience**: Dropshippers and aspiring entrepreneurs.
        * **Value Proposition**: Identifies trending products across multiple e-commerce platforms based on sales velocity and review sentiment, helping users find profitable products to sell.
        * **Monetization Strategy**: Freemium model. Basic trend data is free, while detailed analytics and historical data require a premium subscription.
        """)