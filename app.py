import gradio as gr
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain.utilities import PythonREPL

from templates.templates import TEMPLATE_SQL, TEMPLATE_PLOT
from utils import load_sf_account

PROMPT_SQL = PromptTemplate(
    input_variables=["input", "table_info", "dialect"],
    template=TEMPLATE_SQL,
)

PROMPT_CODE = PromptTemplate(
    input_variables=["input"],
    template=TEMPLATE_PLOT,
)


def run_sql_query(uri, openai_key, table_name, query):
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


def run_py_query(openai_key, query):
    llm = OpenAI(temperature=0, openai_api_key=openai_key)
    chain = LLMChain(llm=llm, prompt=PROMPT_CODE)
    out = chain.run(query)
    return out


def eval_py(code):
    python_repl = PythonREPL()
    return python_repl.run(code)


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

        # Build the query
        sf_table = gr.Textbox(label="Table name to query", value="conversions_demo")
        sf_query = gr.Textbox(label="What is your question?")
        answer = gr.Textbox(label="answer")

        query_button = gr.Button("Run Query")
        query_button.click(
            run_sql_query,
            inputs=[sf_uri, openai_key, sf_table, sf_query],
            outputs=answer,
        )

        # Build the plot code
        plot_query = gr.Textbox(label="plot Query")
        plot_button = gr.Button("Build Plotting code")
        plot_button.click(
            run_py_query,
            inputs=[openai_key, answer],
            outputs=plot_query,
        )

        # Plot the result
        gr.Markdown("## Plot")
        plot = gr.Plot()

        plot_button_2 = gr.Button("Plot!")
        plot_button_2.click(
            eval_py,
            inputs=[plot_query],
            outputs=plot,
        )

        #
        # TODO
        # sf_table = gr.Textbox(label="Table name to query")
        # sf_query = gr.Textbox(label="What is your question?")


demo.launch()
