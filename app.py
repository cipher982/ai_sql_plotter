import os

import gradio as gr
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

_TEMPLATE_SQL = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}

If someone asks for the table events, they really mean the crm.events.recs_events table.

Important: all the SQL queries should be run using ONLY Snowflake specific syntax and commands.
Please make sure all SQL code is specific to Snowflake, and not generic SQL.

Extra information:
- event_type holds the type of event, such as 'attributed_conversion' or 'conversion' or 'bt_rec_served'
- bsin - user id
- use filter site_id = 'citibank' if not specified
- please use current_date() to calculate the current date, do not assume the year is 2021, or any other year you think it is
- be sure to use quotes around strings, such as 'citibank' or INTERVAL '2 MONTH'
- try to avoid nested aggregrations
- use temp tables, instead of subqueries or nested queries
- impressions are referred to in the data as bt_rec_served
- conversion_rate can be calculated by dividing conversion counts by bt_rec_served counts event types

Again: please make sure all code is specific to snowflake

Example:
SELECT 
  COUNT(*) AS postimpression_count, 
  COUNT(CASE WHEN attribution_type = 'POSTCLICK' THEN 1 END) AS postclick_count 
FROM 
  crm.events.recs_events 
WHERE 
  event_type = 'attributed_conversion' AND site_id = 'citibank';

Begin!

Question: {input}"""
PROMPT_SQL = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=_TEMPLATE_SQL
)


def load_sf_account():
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    database = os.getenv("SNOWFLAKE_DATABASE")
    schema = os.getenv("SNOWFLAKE_SCHEMA")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    openai_key = os.getenv("OPENAI_API_KEY")

    # Or get details from .env file
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("SNOWFLAKE_ACCOUNT"):
                account = line.split("=")[1].strip()
            elif line.startswith("SNOWFLAKE_USER"):
                user = line.split("=")[1].strip()
            elif line.startswith("SNOWFLAKE_PASSWORD"):
                password = line.split("=")[1].strip()
            elif line.startswith("SNOWFLAKE_DATABASE"):
                database = line.split("=")[1].strip()
            elif line.startswith("SNOWFLAKE_SCHEMA"):
                schema = line.split("=")[1].strip()
            elif line.startswith("SNOWFLAKE_WAREHOUSE"):
                warehouse = line.split("=")[1].strip()
            elif line.startswith("OPENAI_API_KEY"):
                openai_key = line.split("=")[1].strip()
    uri = f"snowflake://{user}:{password}@{account}/{database}/?warehouse={warehouse}&schema={schema}"
    return account, user, password, database, schema, warehouse, uri, openai_key


def run_query(uri, openai_key, query):
    if isinstance(uri, list):
        uri = uri[0]
    if "textbox" not in uri:
        print("uri is not None", uri)
        print("Loading database. . .")
        db = SQLDatabase.from_uri(uri, include_tables=["recs_events"])
        llm = OpenAI(temperature=0, openai_api_key=openai_key)
        print(f"Loaded database: {db}, for uri: {uri}")
        print("Loading database chain. . .")
        db_chain = SQLDatabaseChain(
            llm=llm, database=db, prompt=PROMPT_SQL, verbose=True
        )
        print("Loaded database chain")
        out = db_chain.run(query)
        return out
    else:
        print("uri is not populated yet: ", uri)
        return None


with gr.Blocks() as demo:
    with gr.Tab("Query"):
        # Account details
        sf_account = gr.Textbox(label="Snowflake Account")
        sf_user = gr.Textbox(label="Snowflake User")
        sf_password = gr.Textbox(label="Snowflake Password")
        sf_database = gr.Textbox(label="Snowflake Database")
        sf_schema = gr.Textbox(label="Snowflake Schema")
        sf_warehouse = gr.Textbox(label="Snowflake Warehouse")
        sf_uri = gr.Textbox(label="Snowflake URI")

        openai_key = gr.Textbox(label="OpenAI API Key")

        load_btn = gr.Button("Load Snowflake Details")
        outputs = [
            sf_account,
            sf_user,
            sf_password,
            sf_database,
            sf_schema,
            sf_warehouse,
            sf_uri,
            openai_key,
        ]
        load_btn.click(fn=load_sf_account, outputs=outputs)

        sf_query = gr.Textbox(label="What is your question?")
        answer = gr.Textbox(label="answer")

        query_button = gr.Button("Query Button")
        query_button.click(
            run_query,
            inputs=[sf_uri, openai_key, sf_query],
            outputs=answer,
        )

        # TODO
        # sf_table = gr.Textbox(label="Table name to query")
        # sf_query = gr.Textbox(label="What is your question?")


demo.launch()
