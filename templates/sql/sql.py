from langchain.prompts import PromptTemplate


sql_full = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples in the database.

Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.

Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Important: all the SQL queries should be run using ONLY {dialect} specific syntax and commands.
Please make sure all SQL code is specific to {dialect}, and not generic SQL. Only use select statements, do not use create, insert, update, delete, etc.

Extra information:
- bsin is the user id
- use the dt column for any time or date filters.
- please use current_date() to calculate the current date, do not assume the year is 2021, or any other year you think it is
- use dateadd instead of interval
- try to avoid nested aggregrations
- use temp tables, instead of subqueries or nested queries
- do not return too much data, if you are asked for the top 10, only return the top 10
- limit results output if data is too large, try and summarize the data.

Only use the tables listed below.

{table_info}

Begin!

Question: {input}"""


sql_prompt = PromptTemplate(
    input_variables=["input", "table_info", "dialect", "top_k"],
    template=sql_full,
)
