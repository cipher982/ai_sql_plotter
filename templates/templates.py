TEMPLATE_SQL = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
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


TEMPLATE_PLOT = """Given a set of input data, plot the data using the following example as a guide:

Input: "The weekly conversion numbers for the past 2 months are 4003, 8678, 9073, 10691, 9807, 9875, 10598, 11457, 7957, and 2239."
Answer: "import matplotlib.pyplot as plt

data = [4003, 8678, 9073, 10691, 9807, 9875, 10598, 11457, 7957, 2239]

plt.figure(figsize=(7, 3))
plt.plot(data)

plt.title('Weekly Conversion Numbers')
plt.xlabel('Week')
plt.ylabel('Number of Conversions')

plt.show()
"

Input: "42118 new users and 28398 return users."
Answer: "import matplotlib.pyplot as plt

new_users = 42118
return_users = 28398

plt.figure(figsize=(7, 3))
plt.bar(['New Users', 'Return Users'], [new_users, return_users])

plt.title('New vs Return Users')
plt.ylabel('Number of Users')

plt.show()
"

Important notes:
- This must be valid python code
- try to use matplotlib for plotting
- do not use any libraries that are not already installed in the environment
- keep the code as simple as possible
- try and use plt.figure(figsize=(7, 3)) to not make the plot too big

begin!

Input: {input}
Answer:"""
