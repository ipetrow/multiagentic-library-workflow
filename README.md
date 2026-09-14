# Project Overview
This project evolves a previous [AI agentic two-step workflow](https://github.com/ipetrow/agentic-bookslog-workflow.git) into an autonomous, multi-agent library management application. It is built around **MCP**, **Anthropic Claude Messages API**, **Agentic Skills**, **SQLite** and **Python**. The LLM capabilities are being utilized through an interactive chat session and further extended by Skills, tools and resources. An observability layer is included to provide an insight on application's flow of events.

# Use Case
The application helps users to manage a digital representation of their personal library and analyze their collection for providing reading habits insights. 

The following scenarios are supported: 
- Retrieve books data from a PDF receipt and input the data to the library.
- Direct prompt queries for book insertion to the library.
- Manage book reading statuses.
- Analyze books data and present it in the form of charts.

## Example Interactions
Through a chat session the users can interact with the application using a natural language.
- "Import the following book -  ..."
- "Import the books from the receipt"
- "Update the reading status of the book with title ... to completed"
- "Show the statistics for books read in 2026"

# Implementation Scope
The goals of the implementation was to design an agent system **without a high-level agent framework**. It explores the following concepts:
- Designing a multi-agent autonomous system.
- Agent-to-Agent delegation.
- Extending agents' capabilities with Agentic Skills.
- Separation of responsibilities between agents.
- Exploring the human-in-the-loop design concept for ensuring data integrity.
- Using the *planning agentic* design pattern to break down tasks into executable steps and avoid unintended outcomes.

All topics were considered with clean architectural principles in mind. Isolating the LLM layer provides flexibility in choosing a different LLM provider based on the agents' specialization. 

## Out of Scope
- Extracting data from multiple files: The workflow handles a single pdf document.

# Project Structure
The application entry point `__main__.py` and codebase is situated in `src/app/`. It consists of the following directories.
- `adapters/`: External interfaces for the application.
    - `llm/`: The LLM related logic - API calls, requests data mapping.
    - `mcp/`: The MCP Client-Server logic - client-server session creation and management, handling server primitives access.
- `agents/`: All the available agents - main library management agent and the specialized subagents.
- `services/`: Capabilities exposed to the LLM through manually defined host tools.
- `skills/`: Logic for managing all the available skills.
- `prompts/`: Contains the agents' system prompts and regular prompts for strictly defined single LLM requests. 
- `schemas/`: Schemas describing host tools exposed to the LLM.
- `tools/`: Logic for managing all the mcp and custom host tools.
- `domain/`: Contains the main data structures for the application domain.
- `observability/`: A layer that an insight on application's flow of events during execution.

Additionally, there are several helper directories:
- `scripts/skills/`: Standalone scripts for managing the Agentic Skills.
- `skills/`: The Skills used by the LLM.
- `config/`: Currently contains a single `skills.json` file describing all the skills used by the LLM.
- `output/`: Contains the output files - generated charts and execution logs.

# Prerequisites
- Installed Python version 3.14.2 or higher.
- Installed Python `uv` package and project management tool. A basic understanding of how the tool works would be helpful for a better insight of how the project is set up and executed.
- Installed the *Anthropic Python SDK*. 
- An Anthropic API key included in the environment variables.

# Implementation Details
## AI Agents
The system includes the following AI agents:
1. *Library Management* AI Agent
    - Responsible for interacting with the user.
    - Coordinates the delegation of tasks to specialized subagents.
    - Plans tasks execution steps.
    - Performs unspecialized tasks, requesting tool executions when necessary.
    - Answers general questions.
2. *Analysis* AI Subagent
    - Analyzes the available books database data based on the user's query.
    - Provides an analysis summary in the form of charts and text.

## Agentic Skills
The Skills are managed by a `SkillRegistry` which loads all available skills described in the `config/skills.json` file. For more details regarding the file creation, check the `Uploading Skills` section below.

The system includes the following Agentic Skills:
- `insert-books`: A Skill with precise step-by-step instructions for inserting books to the library database.
- `data-visualization`: A Skill guiding the representation of analysed data in the form of charts. 

## Tools
The application recognizes two types of tools:
1. MCP tools: These tools are provided by the MCP layer. Their schemas are automatically generated. For detailed tools information check the `MCP Servers` section below.
2. Host tools: These are standalone tools, not part of the MCP Servers. The schemas are manually defined in `src/app/schemas/`. Their purpose is to increase the AI agents' capabilities in making autonomous decisions.
    - `retrieve_receipt_books`: A host tool that can be requested from the *Library Management* AI Agent for retrieving books data from a receipt. It is an encapsulation of the `RetrieveReceiptBooksService` service which processes an MCP resource primitive. In this way, the AI Agent can autonomously decide, based on the user's request, when such action is needed.
    - `delegate_analysis`: A host tool that can be requested from the *Library Management* AI Agent for delegating an analysis task to the *Analysis* AI Subagent. The tool uses the `DelegateAnalysisService`.
    - `generate_bar_chart`: A host visualization tool that generates a horizontal bar chart presenting the reading analytics for a specified year. The tool encapsulates the `GenerateBarChartService` service. 

**Example of a Horizontal Bar Chart - Books Read Per Month (2026)**

![Example of a Horizontal Bar Chart - Books Read Per Month (2026)](output/charts/books-read-per-month-(2026)_2026-08-31_21-02-45.png)

### Tool Management
Each AI Agent has access to a specific set of tools. This deliberate permission constraint ensures *clear responsibility* and increased database *safety*. For example, the *Analysis* AI Subagent is not able to modify the database but only to request read-only operations. Database manipulations are strictly constrained to the *Library Management* AI Agent.

Both, the *Library Management* AI Agent and the *Analysis* AI Subagent, have a `ToolRegistry` instance used to manage the specific tools available. 

## Services
The system includes the following services:
- `RetrieveReceiptBooksService`: The service consists of two steps. It first gets the MCP receipt resource. Afterwards, it makes a single LLM request for retrieving all the books in the provided file.
- `DelegateAnalysisService`: The service delegates an analysis task to the *Analysis* AI Subagent.
- `GenerateBarChartService`: The service creates a horizontal bar chart based on the retrieved data. Except the reading information, retrieved from the database grouped by month, the chart title and labels are provided by the LLM. The charts are being saved in `output/charts` as PNGs.

## API
For the API layer, a MCP Client-Server standard is being used. The MCP Servers are created using `FastMCP` with `stdio` as transport layer. 

### MCP Servers
There are two MCP Servers, each one with its own responsibility:
1. Database server: A MCP Server exposing tools for interacting with the `bookslog` database. 
- Server file path `src/app/adapters/mcp/servers/database/database_server.py`.
- Server resource: An empty `bookslog.db` database situated in the same folder.
- Server primitives: Three tools - `get_all_books() -> str`, `insert_books(book: list[Book]) -> str` and `update_book_reading_status(title: str, author: str, reading_status: ReadingStatus, new_reading_status: ReadingStatus)`.
2. Files server: A MCP Server exposing a file as a resource.
- Server file path `src/app/adapters/mcp/servers/files/files_server.py`.
- Server resource: A PDF receipt file containing a receipt for 3 books. It is situated in `src/app/adapters/mcp/servers/files/receipts`.
- Server primitives: A single resource `file://receipts/receipt-001.pdf`.

The information for connecting to the servers is extracted from the `src/app/adapters/mcp/mcp.json` file.

## LLM
The application uses the Anthropic Claude Messages API with the `claude-sonnet-4-6` model deployed in Azure. The Azure Anthropic API key used for the connection with the LLM.

There are two main files containing the logic related with the Anthropic Claude Messages API:
- `app/llm/anthropic_service.py`: Makes a request to the Anthropic Claude Messages API using the Anthropic Python SDK.
- `app/llm/anthropic_mapper.py`: Contains a mapper class which handles many of the LLM API specifics. It is an additional layer which aims to simplify the process of migration to another LLM provider if needed.

## Database
It is a simplistic SQLite database named `bookslog`, consisting of only one  `books` table. The main idea is to store books information - ***isbn***, ***title***, ***author***, ***number of pages***, ***finished month*** and ***reading status***. 

The database path for the production application is set in the `.env` file and loaded right at the beginning of the application start.

**Note**: For convenience and simplicity of the demo, a book can have only one author stored as a string.

## Data Integrity
A main functionality of the application is retrieving books data from a direct user query or a provided receipt. This process is error prone. To ensure the data integrity, before the database insertion operation, multiple layers of validations are being implemented:
- The `insert-books` agentic Skill ensures the retrieved data is consistent and does not contain duplicating entries (e.g. receipt issue).
- A deterministic Python data normalization and extended validation is performed as well. The LLMs make mistakes. Leaving the validation to them only is unreliable.
- Book duplication check in the database layer.

All found data integrity issues are clarified with the user through the active chat session.

## Dependencies
The project uses the following external Python modules: **mcp**, **anthropic**, **pydantic**, **matplotlib**, **pandas**, **python-dotenv**.

# Observability
For each application execution, there is a log file created (in `outputs/logs/`) that lists all the main events - a task (user prompt), agent, tools, LLM request lifecycles and errors. The input and output tokens are also included in the LLM events.

These traces provide an additional layer of confidence that the systes works as expected. Also, this high level overview can help to identify potetial issues easily.

# Running the Project
## Setup
1. Clone the repository: `git@github.com:ipetrow/multiagentic-library-workflow.git`.
2. Sync the project in order to download and install all the required project dependencies and they are up to date: `uv sync`. This will create the project virtual environment (`.venv`) as well.
3. Provide the model name by setting a value for the `MODEL` constant. The modification should be made in `src/app/adapters/llm/anthropic_service.py`.
4. Update the Azure endpoint. The modification should be made in `src/app/adapters/llm/anthropic_service.py`.
5. Double check the LLM API key is added in the environment variables. The variable is retrieved in `src/app/adapters/llm/anthropic_service.py.py` and is with the name `ANTHROPIC_API_KEY`.

## Execution
The application can be started with the command `uv run python -m src.app`.

# Uploading Skills
The project provides an option to manage the Skills used by the LLM. Dedicated scripts for uploading, deleting and listing all available skills can be found in `scripts/skills/`.

## Setup
1. Similarly to the project setup, the LLM API key and the Azure endpoint should be provided in `scripts/skills/skills_service.py`.
2. Ensure the Skill for upload is in `skills/` directory and it follows the Anthropic Agentic Skills guidelines for file structure. 

## Execution
For uploading all the Skills in `skills/` execute `uv run python -m scripts.skills.upload_skills.py`. This operation will update the `config/skills.json` file with the proper Skill names and IDs.

# References
The project is an evolution and enhancement of an earlier repository where I developed a multi-step agentic AI workflow for inserting books from a receipt in a personal library database [Agentic Bookslog Workflow](https://github.com/ipetrow/agentic-bookslog-workflow.git).
