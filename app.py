from typing import Any

from langchain import OpenAI, SQLDatabaseChain, SQLDatabase
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain.utilities import PythonREPL
import streamlit as st

# from templates.templates import TEMPLATE_SQL
from templates.python import few_shot_python_template
from templates.sql import sql_prompt
from utils import build_snowflake_uri, get_openai_key, create_db_connection


st.set_option("deprecation.showPyplotGlobalUse", False)





DEFAULT_TABLE = "conversions_demo"


@st.cache_data
def run_sql_query(_db: SQLDatabase, _llm: OpenAI, _prompt: PromptTemplate, query: str) -> Any:
    """
    Takes in a natural language question, uses an LLM to parse the question to a SQL
    query, and runs the SQL query on the database.

    Args:
        _db: A langchain SQLDatabase object representing the database to run the query on.
        _llm: An OpenAI object containing the API key and other parameters for the OpenAI Language Model.
        _prompt: A PromptTemplate object representing the prompt to use for the query.
        query: A string containing the question to answer.

    Returns:
        The result of running the SQL query.

    Raises:
        Exception: If the API call to the OpenAI Language Model fails.
    """
    try:
        db_chain = SQLDatabaseChain(llm=_llm, database=_db, prompt=_prompt, verbose=True)
        out = db_chain.run(query)
        return out

    except Exception as e:
        raise Exception("OpenAI API call failed with error: " + str(e))


@st.cache_data
def run_py_query(_llm: OpenAI, _prompt: PromptTemplate, sql_query: str, sql_answer: str) -> Any:
    """
    Takes in the result of a SQL query, uses an LLM to parse the result to Python code,
    and runs the Python code in a Python REPL.

    Args:
        _llm: An OpenAI object containing the API key and other parameters for the OpenAI Language Model.
        _prompt: A PromptTemplate object containing the prompt to use for the query.
        sql_query: A string containing the original SQL query that was run.
        sql_answer: A string containing the result of running the SQL query. To be used as input to the LLM.

    Returns:
        The result of running the Python code.

    Raises:
        Exception: If the API call to the OpenAI Language Model fails.
    """
    # Initialize LLMChain
    py_chain = LLMChain(llm=_llm, prompt=_prompt, verbose=True)

    # Run query using OpenAI API
    try:
        out = py_chain.run(sql_answer).strip("'").strip().strip('"')
    except Exception as e:
        raise Exception("OpenAI API call failed with error: " + str(e))

    # Show the Python code that was generated
    st.write("### Code")
    st.code(out)

    # Run the output code in Python REPL and return the result
    python_repl = PythonREPL()
    return python_repl.run(out)


def start(db, llm, sql_prompt, py_prompt, query):
    """
    Main function for the Streamlit app. Combines the functions run_sql_query and run_py_query,
    and displays the result below.

    Args:
        db: A langchain SQLDatabase object representing the database to run the query on.
        llm: An OpenAI object containing the API key and other parameters for the OpenAI Language Model.
        sql_prompt: A PromptTemplate object representing the prompt to use for the SQL query.
        py_prompt: A PromptTemplate object representing the prompt to use for the Python code.
        query: A string containing the question to answer.

    Returns:
        None
    """
    answer = run_sql_query(db, llm, sql_prompt, query)
    st.write(answer)
    fig = run_py_query(llm, py_prompt, query, answer)
    st.write("### Plot")

    try:
        st.pyplot(fig)
    except TypeError as e:
        st.write("Error displaying plot, try a different question: \n" + str(e))


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
    """
    Streamlit app for the ZMP AI SQL Demo. Allows users to enter a natural language
    question, which is parsed to a SQL query, run on the database, and parsed to
    Python code, which is then run in a Python REPL. The result is a plot.
    """

    st.image("./static/logoPrimary.png")
    st.title("ZMP AI SQL Demo")

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

    st.markdown("## Answer")
    if go_button_1:
        start(db, llm, sql_prompt, few_shot_python_template, defined_query)

    if go_button_2:
        start(db, llm, sql_prompt, few_shot_python_template, open_query)


if __name__ == "__main__":
    main()
