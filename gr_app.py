import gradio as gr
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain.utilities import PythonREPL

from templates.templates import TEMPLATE_SQL, TEMPLATE_PLOT
from utils import build_connections

PROMPT_SQL = PromptTemplate(
    input_variables=["input", "table_info", "dialect"],
    template=TEMPLATE_SQL,
)

PROMPT_CODE = PromptTemplate(
    input_variables=["input"],
    template=TEMPLATE_PLOT,
)

DEFAULT_TABLE = "conversions_demo"


def run_sql_query(query):
    print("Loading database chain. . .")
    db_chain = SQLDatabaseChain(
        llm=llm,
        database=db,
        prompt=PROMPT_SQL,
        verbose=True,
    )
    print("Loaded database chain")
    out = db_chain.run(query)
    return out


def run_py_query(query):
    # Build code
    py_chain = LLMChain(
        llm=llm,
        prompt=PROMPT_CODE,
        verbose=True,
    )
    out = py_chain.run(query)

    # Run code
    python_repl = PythonREPL()
    return python_repl.run(out)


# Connect to database
sf_uri, openai_key = build_connections()
db = SQLDatabase.from_uri(sf_uri, include_tables=[DEFAULT_TABLE])

# Start the LLMs
llm = OpenAI(temperature=0, openai_api_key=openai_key)


with gr.Blocks() as demo:
    # img = gr.Image("static/title.svg").style(height="8", width="12")
    gr.Markdown("# Querying SQL with AI")

    #################
    ### SQL Query ###
    #################
    gr.Markdown("## Query")

    sf_table = gr.Textbox(label="Table name to query", value="conversions_demo")
    sf_query = gr.Textbox(label="What is your question?")
    answer = gr.Textbox(label="answer")

    query_button = gr.Button("Run Query")
    query_button.click(
        run_sql_query,
        inputs=[sf_query],
        outputs=answer,
    )

    ####################
    ### Python Query ###
    ####################
    gr.Markdown("## Plot")

    # Take SQL results and plot with Python
    plot = gr.Plot()
    plot_button = gr.Button("Plot!")
    plot_button.click(
        run_py_query,
        inputs=[answer],
        outputs=plot,
    )


demo.launch()
