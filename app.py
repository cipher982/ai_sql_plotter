import datetime
from typing import Any

from langchain import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.llms import OpenAI, OpenAIChat
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain, SQLDatabaseChain
from langchain.utilities import PythonREPL
import pandas as pd
import streamlit as st

from templates.python.prompts import few_shot_python_prompt, fix_code_prompt
from templates.sql.sql import sql_prompt
from utils import build_snowflake_uri, get_openai_key, create_db_connection


st.set_option("deprecation.showPyplotGlobalUse", False)

DEFAULT_TABLES = ["citi_conversions_demo", "citi_impressions_demo"]


# @st.cache_data
def run_sql_query(_db: SQLDatabase, _llm: OpenAI, _prefix: str, query: str, use_agent: bool) -> Any:
    """
    Takes in a natural language question, uses an LLM to parse the question to a SQL
    query, and runs the SQL query on the database.

    Args:
        _db: A langchain SQLDatabase object representing the database to run the query on.
        _llm: An OpenAI object containing the API key and other parameters for the OpenAI Language Model.
        _prefix: A string containing the prefix to use for the prompt.
        query: A string containing the question to answer.

    Returns:
        The result of running the SQL query.

    Raises:
        Exception: If the API call to the OpenAI Language Model fails.
    """
    if use_agent:
        toolkit = SQLDatabaseToolkit(db=_db)
        agent = create_sql_agent(llm=_llm, toolkit=toolkit, prefix=_prefix, verbose=True)
        result = agent.run(query)
    else:
        chain = SQLDatabaseChain(
            llm=_llm,
            database=_db,
            prompt=_prefix,
            return_direct=False,
            return_intermediate_steps=True,
        )
        out = chain(query)
        result = out["result"]
        sql_code = out["intermediate_steps"][0]
        st.write("### SQL Code")
        st.code(sql_code)
        result_data = out["intermediate_steps"][1]
        st.write("### Data")
        result_object = eval(result_data)
        result_df = pd.DataFrame(result_object)
        st.dataframe(result_df)

    return result


# @st.cache_data
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

    # Use LLMChain to generate Python code
    try:
        plotting_code = py_chain.run(sql_answer).strip("'").strip().strip('"')
    except Exception as e:
        raise Exception("OpenAI API call failed with error: " + str(e))

    # Show the Python code that was generated
    st.write("### Python Code")
    st.code(plotting_code)

    try:
        # Run the Python code and build a figure
        python_repl = PythonREPL()
        fig = python_repl.run(plotting_code)
    except Exception as e:
        st.write("Error running Python code, trying again")

        # If the code fails, try to fix it
        fix_chain = LLMChain(llm=_llm, prompt=fix_code_prompt, verbose=True)
        plotting_code_fixed = fix_chain.run([plotting_code, e]).strip("'").strip().strip('"')

        # Run the fixed code
        python_repl = PythonREPL()
        fig = python_repl.run(plotting_code_fixed)

    return fig


def start(db, llm, sql_prompt, py_prompt, query, use_agent):
    """
    Main function for the Streamlit app. Combines the functions run_sql_query and run_py_query,
    and displays the result below.

    Args:
        db: A langchain SQLDatabase object representing the database to run the query on.
        llm: An OpenAI object containing the API key and other parameters for the OpenAI Language Model.
        sql_prompt: The the prompt to use for the SQL query.
        py_prompt: A PromptTemplate object representing the prompt to use for the Python code.
        query: A string containing the question to answer.

    Returns:
        None
    """
    answer = run_sql_query(db, llm, sql_prompt, query, use_agent)
    st.write("### Answer")
    st.write(answer)

    fig = run_py_query(llm, py_prompt, query, answer)
    st.write("### Plot")

    try:
        st.pyplot(fig)
    except TypeError as e:
        st.write("Error displaying plot, try a different question: \n" + str(e))


# Streamlit app
def main():
    """
    Streamlit app for the ZMP AI SQL Demo. Allows users to enter a natural language
    question, which is parsed to a SQL query, run on the database, and parsed to
    Python code, which is then run in a Python REPL. The result is a plot.
    """

    st.image("./static/logoPrimary.png")
    st.title("ZMP AI SQL Demo")

    # Grab connection details
    sf_uri = build_snowflake_uri()

    # Get openai key
    openai_key = get_openai_key()

    # Connect to the database
    db = create_db_connection(sf_uri, DEFAULT_TABLES)

    # "with" notation
    with st.sidebar:
        model_selection = st.radio("Choose a model", ("GPT3", "ChatGPT"))
        if model_selection == "GPT3":
            llm = OpenAI(model_name="text-davinci-003", temperature=0, openai_api_key=openai_key)
        elif model_selection == "ChatGPT":
            llm = OpenAIChat(temperature=0, openai_api_key=openai_key)
        else:
            raise ValueError("Invalid model selection")

        use_agent = st.checkbox("Use Agent (experimental)", value=False)

        # Configure DB connections
        tables_to_use = st.multiselect(
            "Choose tables to use",
            DEFAULT_TABLES,
        )

    st.markdown("# Query")
    # create a drop down menu with pre-defined queries
    defined_query = st.selectbox(
        "Select a pre-defined query",
        [
            "What are the weekly conversion numbers for the past 2 months?",
            "What are the names and total numbers for the top 5 resources?",
            "What are the top 10 dmas by conversion counts?",
            "What is the breakdown in device types that convert?",
        ],
    )
    go_button_1 = st.button("Go")

    open_query = st.text_input("Or, enter a custom query")
    go_button_2 = st.button("Go ")

    st.markdown("# Results")
    if go_button_1:
        start(db, llm, sql_prompt, few_shot_python_prompt, defined_query, use_agent)

    if go_button_2:
        start(db, llm, sql_prompt, few_shot_python_prompt, open_query, use_agent)


if __name__ == "__main__":
    main()
