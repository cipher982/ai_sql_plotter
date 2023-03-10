import os
from typing import Optional

from langchain import SQLDatabase
import streamlit as st


class MissingEnvironmentVariableError(Exception):
    pass


@st.cache_data
def build_snowflake_uri() -> str:
    """
    Creates the Snowflake URI from environment variables or a `.env` file.

    Returns:
        A string containing the Snowflake connection URI.
    Raises:
        MissingEnvironmentVariableError: If any of the required environment variables are missing or empty.
    """
    required_env_vars = [
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_SCHEMA",
        "SNOWFLAKE_WAREHOUSE",
        "SNOWFLAKE_ROLE",
    ]

    env_vars = {env_var: os.getenv(env_var) for env_var in required_env_vars}

    for env_var, var_name in zip(required_env_vars, env_vars.keys()):
        if not env_vars[env_var]:
            raise MissingEnvironmentVariableError(f"{env_var} is missing")

    uri = (
        f"snowflake://{env_vars['SNOWFLAKE_USER']}:{env_vars['SNOWFLAKE_PASSWORD']}@{env_vars['SNOWFLAKE_ACCOUNT']}/"
        f"{env_vars['SNOWFLAKE_DATABASE']}/?warehouse={env_vars['SNOWFLAKE_WAREHOUSE']}&schema={env_vars['SNOWFLAKE_SCHEMA']}"
        f"&role={env_vars['SNOWFLAKE_ROLE']}"
    )

    return uri


def get_openai_key() -> Optional[str]:
    """
    Retrieves the OpenAI API key from the environment variable OPENAI_API_KEY.

    Returns:
        The OpenAI API key as a string, or None if the environment variable is not set.
    """
    key = os.environ.get("OPENAI_API_KEY")

    if not key:
        raise Exception("Missing OPENAI_API_KEY environment variable")

    return key


@st.cache_resource
def create_db_connection(uri: str, include_tables: list) -> SQLDatabase:
    """
    Creates a Snowflake database connection from a URI.

    Args:
        uri: A string containing the Snowflake URI.
    Returns:
        A `Database` object.
    """
    db = SQLDatabase.from_uri(
        uri,
        include_tables=include_tables,
    )
    return db


def detect_malicious_sql_query(query: str) -> bool:
    """
    Detects if a SQL query is malicious by checking if it contains any of the following keywords:
    - DROP
    - TRUNCATE
    - DELETE
    - ALTER
    - CREATE
    - GRANT
    - REVOKE
    - RENAME
    - UPDATE
    - INSERT

    Args:
        query: A string containing the SQL query to check.

    Returns:
        A boolean indicating if the query is malicious.
    """
    malicious_keywords = [
        "DROP",
        "TRUNCATE",
        "DELETE",
        "ALTER",
        "CREATE",
        "GRANT",
        "REVOKE",
        "RENAME",
        "UPDATE",
        "INSERT",
    ]

    for keyword in malicious_keywords:
        if keyword in query.upper():
            return True

    return False
