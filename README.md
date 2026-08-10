# Project Overview
TODO

# Use Cases
TODO 

# Implementation Scope
TODO

## Out of Scope
- Extracting data from multiple files: The workflow handles a single pdf document. 

# Project Structure
The appication entry point `__main__.py` and codebase is situated in `src/app`. It consists of the following subdirectories.
- `adapters/`: External interfaces for the application.
    - `llm/`: The LLM related logic - API calls, requests data mapping.
    - `mcp/`: The MCP Client-Server logic - client-server session creation and management, handling server primitives access.
- `agents/`: All the available agents - main library management agent and the specialized subagents.
- `services/`: Capabilities exposed to the LLM through a manualy defined host tools.
- `skills/`: Logic for managing all the available skills.
- `prompts/`: Contains the agents' system prompts and regular prompts for strinctly defined single LLM requests. 
- `schemas/`: Schemas describing host tools exposed to the LLM.
- `tools/`: Logic for managing all the available skills - mcp and custom host tools.
- `domain/`: Contains the main data structures for the application domain concepts.

Additionaly, there are several helper directories:
- `scripts/skills/`: Standalone scripts for managing the Agentic Skills.
- `skills/`: The Skills used by the LLM.
- `config/`: Currently contains a single `skills.json` file describing all the skills used by the LLM.

# Prerequisites
- Installed Python version 3.14.2 or higher.
- Installed Python `uv` package and project management tool. A basic understanding of how the tool works would be helpful for a better insight of how the project is set up and executed.
- Installed the *Anthropic Python SDK*. 
- An Anthropic API key included in the environment variables.

# Implementation Details
## Agents

TODO

### Skills

### Tools

### Services

## API
For the API layer, a MCP Client-Server standard is being used. The MCP Servers are created using `FastMCP` with `stdio` as transport layer. 

### Servers
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
- `app/llm/anthropic_mapper.py`: Contains a mapper class which handles many of the LLM API specifics. It is an additional layer which aims to simlify the process of migration to another LLM provider if needed.

## Database
It is a simplistic SQLite database named ***bookslog***, consisting of only one  ***books*** table. The main idea is to store books information - ***isbn***, ***title***, ***author***, ***number of pages*** and ***reading status***. For convenience and simplicity of the demo, a book can have only one author stored as a string.

The database path for the production application is set in the `.env` file and loaded right at the beginning of the application start.

# Running the Project
## Setup
1. Clone the repository: `git@github.com:ipetrow/multiagentic-library-workflow.git`.
2. Sync the project in order to download and install all the required project dependencies and they are up to date: `uv sync`. This will create the project virtual environment (`.venv`) as well.
3. Provide the model name by setting a value for the `MODEL` constant. The modification should be made in `src/app/adapters/llm/anthropic_service.py`.
4. Update the Azure endpoint. The modification should be made in `src/app/adapters/llm/anthropic_service.py`.
5. Double check the LLM API key is added in the environment variables. The variable is retrieved in `src/app/adapters/llm/anthropic_service.py.py` and is with the name `ANTHROPIC_API_KEY`.

## Execution
Start the MCP Client and connect to the MCP Server by: `uv run python -m src.app`.

# Uploading Skills
The project provides the option to manage the Skills used by the LLM. Dedicated scripts for uploading, deleting and listing all available skills can be found in `scripts/skills/`.

## Setup
1. Similarly to the project setup, the LLM API key and the Azure endpoint should be provided in `scripts/skills/skills_service.py`.
2. Ensure the Skill for upload is in `skills/` directory and it follows the Anthropic Agentic Skills guidelines for file structure. 

## Execution
For uploading all the Skills in `skills/` execute `uv run python -m scripts.skills.upload_skills.py`.

# References
The project is an evolution and enhancement of an earlier repository where I developed a multi-step agentic AI workflow for inserting bookds from a receipt in a personal library database [Agentic Bookslog](git@github.com:ipetrow/agentic_bookslog.git).
