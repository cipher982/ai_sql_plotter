import os

import gradio as gr


def load_sf_account():
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    database = os.getenv("SNOWFLAKE_DATABASE")
    schema = os.getenv("SNOWFLAKE_SCHEMA")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")

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

    return account, user, password, database, schema, warehouse


with gr.Blocks() as demo:
    with gr.Tab("Account Details"):
        sf_account = gr.Textbox(label="Snowflake Account")
        sf_user = gr.Textbox(label="Snowflake User")
        sf_password = gr.Textbox(label="Snowflake Password")
        sf_database = gr.Textbox(label="Snowflake Database")
        sf_schema = gr.Textbox(label="Snowflake Schema")
        sf_warehouse = gr.Textbox(label="Snowflake Warehouse")

        load_btn = gr.Button("Load Snowflake Details")
        outputs = [
            sf_account,
            sf_user,
            sf_password,
            sf_database,
            sf_schema,
            sf_warehouse,
        ]
        load_btn.click(fn=load_sf_account, outputs=outputs)

    with gr.Tab("Query"):
        sf_table = gr.Textbox(label="Table name to query")
        sf_query = gr.Textbox(label="What is your question?")
        inputs = [
            sf_account,
            sf_user,
            sf_password,
            sf_database,
            sf_schema,
            sf_warehouse,
        ]
        output = gr.Textbox(label="Output Box")


demo.launch()
