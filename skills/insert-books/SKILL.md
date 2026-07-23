---
name: insert-books
description: Extracts books data from a receipt file and imports the extracted data in a database.
---

# Inserting Books
Automated workflow for extracting books data from a PDF receipt and inserting it into a database functionings as a books library repository. 

## Workflow

TODO: General guidance: be concise - no lengthy explanations 

### Step 1: Plan Execution

Before performing any action, return a step-by-step plan to carry out the user's request. Include a description of the expected MCP tools and resources to be used.

Wait for User confirmation before continuing with the plan execution.

### Step 2: Extract Books Data

For each book in the PDF receipt resource extract the following data:

- isbn
- title
- author
- number of pages

**Guidelines**
- When a book has multiple authors, extract only the first one listed.
- The extracted data should be used for all subsequent steps in the workflow.
- All fields are required. In case of a missing or unclear fields in the PDF resource DO NOT try to assume or fill these information. Consider the PDF as a single source of truth.

### Step 3: Assert Extracted Books Data

Assert the extracted book data values for

- Data duplication
- Missing required data

If the assertion fails, terminate the workflow execution and notify the User for the issue.

### Step 4: Apply Data Rules

For each extracted book add a `reading status` field with a default value of `not_started`. It represets that the book is new and yet to be read by the User.   

### Step 5: Insert the Extracted Books Data into the Database

Insert the extracted books into the database.

**Guidance**
- Use the available MCP tools to perform the required actions. For the required tool's arguments use the earlier extracted information. 
- Provide a short reasoning why you need the MCP tools.

Once the books are inserted, ensure that the operation has been successful by querying the database.

**Database Schema**
| Column | Type | Description |
|--------|------|-------------|
| isbn | INTEGER | Book's isbn |
| title | TEXT | Book's title |
| author | TEXT | Book's author |
| pages_num | INTEGER | Book's number of pages |
| reading_status | TEXT | Book's reading status (allowed values: 'not_started' 'in_progress', 'completed', 'paused', 'did_not_finish') |

### Step 6: Report to User

Communicate clearly whether the task has been successful or not. If yes, summarize
- the extracted books data
- the data inserted into the database
- faced issues in the process