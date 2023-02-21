import os

import gradio as gr
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

from templates.templates import _TEMPLATE_SQL


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
        with gr.Accordion("See Details"):
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
