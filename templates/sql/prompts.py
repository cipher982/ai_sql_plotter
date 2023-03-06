from langchain.prompts.prompt import PromptTemplate

from templates.sql.templates import sql_full, sql_minimal


sql_prompt = PromptTemplate(
    input_variables=["input", "table_info", "dialect"],
    template=sql_full,
)

sql_minimal_prompt = PromptTemplate(
    input_variables=["dialect"],
    template=sql_minimal,
)
