_TEMPLATE_SQL = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
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
- event_type holds the type of event, such as 'attributed_conversion' or 'conversion' or 'bt_rec_served'
- bsin - user id
- use filter site_id = 'citibank' if not specified
- please use current_date() to calculate the current date, do not assume the year is 2021, or any other year you think it is
- be sure to use quotes around strings, such as 'citibank' or INTERVAL '2 MONTH'
- try to avoid nested aggregrations
- use temp tables, instead of subqueries or nested queries
- impressions are referred to in the data as bt_rec_served
- conversion_rate can be calculated by dividing conversion counts by bt_rec_served counts event types

Again: please make sure all code is specific to snowflake

Example:
SELECT 
  COUNT(*) AS postimpression_count, 
  COUNT(CASE WHEN attribution_type = 'POSTCLICK' THEN 1 END) AS postclick_count 
FROM 
  crm.events.recs_events 
WHERE 
  event_type = 'attributed_conversion' AND site_id = 'citibank';

Begin!

Question: {input}"""
