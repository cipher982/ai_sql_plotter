from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI, OpenAIChat
from langchain.agents import AgentExecutor
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import SQLDatabaseChain

from utils import build_snowflake_uri, get_openai_key, create_db_connection


tables = ["citi_conversions_demo", "citi_impressions_demo"]

sf_uri = build_snowflake_uri()
openai_key = get_openai_key()
openai_key = get_openai_key()

llm35 = OpenAIChat(
    temperature=0,
    openai_api_key=openai_key,
    streaming=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)
llm3 = OpenAI(
    model_name="text-davinci-003",
    temperature=0,
    openai_api_key=openai_key,
    streaming=True,
    # max_tokens=50,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)
db = create_db_connection(sf_uri, tables)
toolkit = SQLDatabaseToolkit(db=db)


db_chain = SQLDatabaseChain(llm=llm35, database=db)
out = db_chain.run(query="count rows in citi clicks table", return_direct=False)

print(out)
