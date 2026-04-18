from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.schema import AIMessage, HumanMessage
from dotenv import load_dotenv

import re
import os
import psycopg2 as psy
import json

with open('schema.json', 'r') as f:
    schema = json.load(f)

conn = psy.connect(
    host="localhost",
    database="NLP2SQL",
    user="postgres",
    password="GAurav!%!(",
    port="5433"
)


def extract_sql(llm_response: str) -> str | None:
    code_block = re.search(r"```sql\s*(.*?)\s*```", llm_response, re.DOTALL | re.IGNORECASE)

    if code_block:
        return code_block.group(1).strip()

    sql_match = re.search(
        r"(SELECT|INSERT|UPDATE|DELETE|WITH)\s+.*?;",
        llm_response,
        re.DOTALL | re.IGNORECASE
    )

    if sql_match:
        return sql_match.group(0).strip()

    return None

cursor = conn.cursor()

load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv('Google_API_3')

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    temperature = 0
)

system_prompt = """
    You are an expert SQL generator.

    Your job:
    1. Convert user natural language into SQL queries.
    2. If the request is ambiguous, DO NOT guess. Ask clarifying questions.
    3. Use conversation history for context.
    4. Explain assumptions briefly.
    5. The SQL command should be PostgreSQL compliant

    Database Schema:
    {schema}

    Rules:
    - Do NOT hallucinate columns
    - Prefer safe queries (LIMIT when needed)
    - Use standard SQL
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

history = []


def run_chat():
    print("Gemini Model started")

    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            cursor.close()
            break

        history.append(HumanMessage(content = user_input))

        messages = prompt.format_messages(
            history = history,
            input = user_input,
            schema = schema
        )

        response = llm.invoke(messages)

        history.append(AIMessage(content = response.content))

        print("AI Response: ",response.content)

        output = extract_sql(response.content)

        if output is None:
            pass

        else:
            cursor.execute(output)
            ans = cursor.fetchall()
            print("SQL OutPut: ", ans)

run_chat()
