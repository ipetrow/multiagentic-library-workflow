---
name: insert-books
description: Handles the addition of books into the library database. Use when user asks to add books to the personal library, extracted either from a direct prompt or a receipt.
---

# Workflow

## Step 1: Plan Execution
- Present a high-level plan for the task execution and ask the user for confirmation.
- Only after confirmation proceed with the execution.

## Step 2: Data Validation
- Ensure the data is consistent, complete and there are no entry duplications.
- In case of validation errors, ask the user for clarification. Explain which book is affected, what is missing or ambiguous, suggest resolution.
- If optional data is missing, proceed with tool invocation without asking for configrmation.
- Do NOT invent missing book information.

Required Book Fields
- title
- author
- page number

Optional Book Fields
- ISBN
- finished month

## Step 3: Data Insertion
Use the `insert_books` tool for adding the books.

## Step 4: Verify Insertion is Successful
After the insertion operation completes, use available tools to ensure the data has been successfully added.

## Step 5: Report Result
- Communicate concisely whether the task has been successful or not by listing the successful and unsuccessful book additions.
- Do not state unconfirmed operations as successful.
