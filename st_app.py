from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain.utilities import PythonREPL
import streamlit as st

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

# Connect to database
sf_uri, openai_key = build_connections()
db = SQLDatabase.from_uri(sf_uri, include_tables=[DEFAULT_TABLE])

# Start the LLMs
llm = OpenAI(temperature=0, openai_api_key=openai_key)


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


# Streamlit app
def main():
    st.markdown("# Querying SQL with AI")

    #################
    ### SQL Query ###
    #################
    st.markdown("## Query")

    sf_query = st.text_input("What is your question?")
    query_button = st.button("Run Query")

    if query_button:
        answer = run_sql_query(sf_query)
        st.write(answer)

    ####################
    ### Python Query ###
    ####################
    st.markdown("## Plot")

    # Take SQL results and plot with Python
    plot_button = st.button("Plot!")
    if plot_button:
        fig = run_py_query(answer)
        st.pyplot(fig)


if __name__ == "__main__":
    main()
