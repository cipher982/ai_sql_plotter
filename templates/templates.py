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
Please make sure all SQL code is specific to Snowflake, and not generic SQL.

Extra information:
- bsin - user id
- please use current_date() to calculate the current date, do not assume the year is 2021, or any other year you think it is
- be sure to use quotes around strings, such as 'citibank' or INTERVAL '2 MONTH'
- try to avoid nested aggregrations
- use temp tables, instead of subqueries or nested queries
- do not return too much data, if you are asked for the top 10, only return the top 10

Begin!

Question: {input}"""


TEMPLATE_PLOT = """Given a set of input data, plot the data using the following example as a guide:

Input: "[(12179, datetime.datetime(2023, 1, 16, 0, 0, tzinfo=<UTC>)), (54233, datetime.datetime(2023, 1, 23, 0, 0, tzinfo=<UTC>)), (57980, datetime.datetime(2023, 1, 30, 0, 0, tzinfo=<UTC>)), (53337, datetime.datetime(2023, 2, 6, 0, 0, tzinfo=<UTC>)), (49756, datetime.datetime(2023, 2, 13, 0, 0, tzinfo=<UTC>))]'
Answer: "import matplotlib.pyplot as plt
import datetime

data = [(12179, datetime.datetime(2023, 1, 16, 0, 0)),
        (54233, datetime.datetime(2023, 1, 23, 0, 0)),
        (57980, datetime.datetime(2023, 1, 30, 0, 0)),
        (53337, datetime.datetime(2023, 2, 6, 0, 0)),
        (49756, datetime.datetime(2023, 2, 13, 0, 0))]

values = [d[0] for d in data]
dates = [d[1] for d in data]

plt.figure(figsize=(7, 3))

plt.plot(dates, values)

plt.title('Data Plot')
plt.xlabel('Date')
plt.ylabel('Value')

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
