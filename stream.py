from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI, OpenAIChat
from langchain.agents import AgentExecutor

from utils import build_snowflake_uri, get_openai_key, create_db_connection

from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

openai_key = get_openai_key()
llm = OpenAIChat(
    temperature=0,
    openai_api_key=openai_key,
    streaming=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

llm("How can I implement callbacks in python to stream text to streamlit")
