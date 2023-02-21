import gradio as gr
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

from templates.templates import _TEMPLATE_SQL
from utils import load_sf_account

PROMPT_SQL = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=_TEMPLATE_SQL
)


def run_query(uri, openai_key, table_name, query):
    if isinstance(uri, list):
        uri = uri[0]
    if "textbox" not in uri:
        print("uri is not None", uri)
        print("Loading database. . .")
        db = SQLDatabase.from_uri(uri, include_tables=[table_name])
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
    # img = gr.Image("static/title.svg").style(height="8", width="12")
    gr.Markdown("# Querying SQL with AI")
    with gr.Tab("Query"):
        with gr.Accordion("Connection Details"):
            sf_uri = gr.Textbox(label="Snowflake URI")
            openai_key = gr.Textbox(label="OpenAI API Key")

            load_btn = gr.Button("Load Snowflake Details")
            outputs = [
                sf_uri,
                openai_key,
            ]
        load_btn.click(fn=load_sf_account, outputs=outputs)

        sf_table = gr.Textbox(label="Table name to query", value="conversions_demo")
        sf_query = gr.Textbox(label="What is your question?")
        answer = gr.Textbox(label="answer")

        query_button = gr.Button("Query Button")
        query_button.click(
            run_query,
            inputs=[sf_uri, openai_key, sf_table, sf_query],
            outputs=answer,
        )

        # TODO
        # sf_table = gr.Textbox(label="Table name to query")
        # sf_query = gr.Textbox(label="What is your question?")


demo.launch()
