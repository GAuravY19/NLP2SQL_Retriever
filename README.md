# NLP2SQL_Retriever

## Overview

This project is an end-to-end **Natural Language to SQL (NL → SQL)** system built to translate user queries into executable SQL and return database results in a clean, usable format.

The goal was not just to generate SQL, but to build a system that:

* Understands user intent
* Handles ambiguity
* Maintains conversational context
* Produces executable, reliable queries

---

## Architecture

The system follows a simple but effective pipeline:

**User → LLM → SQL Extraction → Database Execution → Final Output**

### Flow Breakdown:

1. **User Input**

   * User provides a natural language query

2. **LLM Processing (Gemini)**

   * The query is passed to Gemini
   * LLM generates a response containing SQL (and sometimes explanations)

3. **SQL Extraction Layer**

   * Response is cleaned
   * Only the SQL query is extracted and retained

4. **Database Execution (PostgreSQL)**

   * Clean SQL is executed on the PostgreSQL database

5. **Final Output**

   * User receives:

     * Generated SQL query
     * Result from database

---

## Capabilities

The system is designed to handle a wide range of query complexities:

* **Simple Queries (Single Table)**
* **Joins (Multi-table queries)**
* **Aggregations + Conditions**
* **Window Functions**
* **Ambiguous Queries (LLM asks for clarification)**
* **Query Caching**
* **Multi-turn Conversations (context-aware)**

---

## Database Design

* Backend: **PostgreSQL**
* Schema is structured and passed to the LLM in a **typed JSON format**
* Includes:

  * Data types
  * Primary keys
  * Foreign keys
  * Enums
  * Defaults

This improves SQL generation accuracy significantly compared to raw schema dumps.

---

## Use of AI (Being Transparent)

This project uses:

* **Gemini** as the primary LLM for SQL generation
* **ChatGPT** as a development assistant

ChatGPT was used to:

* Accelerate development
* Debug issues faster
* Explore better architectural patterns
* Improve prompt design and system structure

---

## Trade-offs & Shortcuts

To keep the system focused and buildable within time constraints, a few trade-offs were made:

### 1. No Column-Level Descriptions

* Current schema only includes data types
* Missing semantic descriptions may cause ambiguity in complex queries

### 2. Terminal-Based Interface

* Interaction is CLI-based
* Not user-friendly for non-technical users

### 3. No Advanced Retrieval (RAG)

* Entire schema is passed instead of dynamically selecting relevant tables

---

## What I Would Do With More Time

### 1. Add Column-Level Semantics

* Improve schema with descriptions
* Reduce ambiguity
* Improve LLM reasoning for edge cases

### 2. Build a Proper Chat Interface

* Convert into a web-based chatbot (Streamlit / React)
* Improve usability and accessibility

### 3. Schema Retrieval Layer (RAG)

* Dynamically fetch only relevant tables
* Improve performance and accuracy

### 4. SQL Validation Loop

* Execute → detect errors → auto-correct via LLM
* Make system more robust

---
