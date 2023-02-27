from langchain.prompts.prompt import PromptTemplate


sql_template = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}

If someone asks for the table events, they really mean the crm.events.recs_events table.

Important: all the SQL queries should be run using ONLY Snowflake specific syntax and commands.
Please make sure all SQL code is specific to Snowflake, and not generic SQL. Only use select statements, do not use create, insert, update, delete, etc.

Extra information:
- bsin - user id
- please use current_date() to calculate the current date, do not assume the year is 2021, or any other year you think it is
- be sure to use quotes around strings, such as 'citibank' or INTERVAL '2 MONTH'
- try to avoid nested aggregrations
- use temp tables, instead of subqueries or nested queries
- do not return too much data, if you are asked for the top 10, only return the top 10
- for the final answer, be sure to include numeric data in the answer, such as "The top 2 dmas by conversion counts are: 1. New York (2045), 2. Los Angeles (1533)"

Begin!

Question: {input}"""

sql_prompt = PromptTemplate(
    input_variables=["input", "table_info", "dialect"],
    template=sql_template,
)