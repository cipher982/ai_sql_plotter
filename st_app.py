from langchain import OpenAI, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain.utilities import PythonREPL
import streamlit as st

from templates.templates import TEMPLATE_SQL, TEMPLATE_PLOT
from utils import build_snowflake_uri, get_openai_key, create_db_connection


st.set_option("deprecation.showPyplotGlobalUse", False)


PROMPT_SQL = PromptTemplate(
    input_variables=["input", "table_info", "dialect"],
    template=TEMPLATE_SQL,
)

PROMPT_CODE = PromptTemplate(
    input_variables=["input"],
    template=TEMPLATE_PLOT,
)

DEFAULT_TABLE = "conversions_demo"


@st.cache_data
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
    out = out.strip("'").strip().strip('"')
    print(out)

    # Run code
    python_repl = PythonREPL()
    return python_repl.run(out)


def start(query):
    answer = run_sql_query(query)
    st.write(answer)
    fig = run_py_query(answer)
    st.pyplot(fig)


# Grab connection details
sf_uri = build_snowflake_uri()

# Get openai key
openai_key = get_openai_key()

# Connect to the LLM
llm = OpenAI(temperature=0, openai_api_key=openai_key)

# Connect to the database
db = create_db_connection(sf_uri)


# Streamlit app
def main():
    st.image("./static/logoPrimary.png")
    st.title("ZMP AI SQL Demo")

    #############
    ### Query ###
    #############
    st.markdown("## Query")

    # create a drop down menu with pre-defined queries
    defined_query = st.selectbox(
        "Select a pre-defined query",
        [
            "What are the weekly conversion numbers for the past 2 months?",
            "What are the names and total numbers for the top 5 resources?",
            "What are the top 10 dmas by conversion counts?",
            "What is the breakdown of return users vs new users?",
        ],
    )
    go_button_1 = st.button("Go")

    open_query = st.text_input("Or, enter a custom query")
    go_button_2 = st.button("Go ")

    ############
    ### PLOT ###
    ############
    st.markdown("## Plot")

    if go_button_1:
        start(defined_query)

    if go_button_2:
        start(open_query)


if __name__ == "__main__":
    main()
