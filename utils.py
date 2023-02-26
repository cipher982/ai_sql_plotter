import os
from typing import Optional

from langchain import SQLDatabase
import streamlit as st


DEFAULT_TABLE = "conversions_demo"


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
    ]

    env_vars = {env_var: os.getenv(env_var) for env_var in required_env_vars}

    for env_var, var_name in zip(required_env_vars, env_vars.keys()):
        if not env_vars[env_var]:
            raise MissingEnvironmentVariableError(f"{env_var} is missing")

    uri = f"snowflake://{env_vars['SNOWFLAKE_USER']}:{env_vars['SNOWFLAKE_PASSWORD']}@{env_vars['SNOWFLAKE_ACCOUNT']}/{env_vars['SNOWFLAKE_DATABASE']}/?warehouse={env_vars['SNOWFLAKE_WAREHOUSE']}&schema={env_vars['SNOWFLAKE_SCHEMA']}"
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
def create_db_connection(uri: str, include_tables: list = [DEFAULT_TABLE]) -> SQLDatabase:
    """
    Creates a Snowflake database connection from a URI.

    Args:
        uri: A string containing the Snowflake URI.
    Returns:
        A `Database` object.
    """
    db = SQLDatabase.from_uri(uri, include_tables=include_tables)
    return db
