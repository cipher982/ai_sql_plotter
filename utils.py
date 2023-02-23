import os

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

    # Or get details from .env file
    # TODO: would love to use dotenv here, but having issues with py3.11
    with open(".env", "r") as f:
        for line in f:
            for env_var in required_env_vars:
                if line.startswith(env_var):
                    env_vars[env_var] = line.split("=")[1].strip()

    for env_var, var_name in zip(required_env_vars, env_vars.keys()):
        if not env_vars[env_var]:
            raise MissingEnvironmentVariableError(f"{env_var} is missing")

    uri = f"snowflake://{env_vars['SNOWFLAKE_USER']}:{env_vars['SNOWFLAKE_PASSWORD']}@{env_vars['SNOWFLAKE_ACCOUNT']}/{env_vars['SNOWFLAKE_DATABASE']}/?warehouse={env_vars['SNOWFLAKE_WAREHOUSE']}&schema={env_vars['SNOWFLAKE_SCHEMA']}"
    return uri


@st.cache_data
def get_openai_key():
    var = "OPENAI_API_KEY"
    with open(".env", "r") as f:
        for line in f:
            if line.startswith(var):
                key = line.split("=")[1].strip()

    if not key:
        raise Exception(f"Missing {var} environment variable")

    return key


@st.cache_resource
def create_db_connection(
    uri: str, include_tables: list = [DEFAULT_TABLE]
) -> SQLDatabase:
    """
    Creates a Snowflake database connection from a URI.

    Args:
        uri: A string containing the Snowflake URI.
    Returns:
        A `Database` object.
    """
    db = SQLDatabase.from_uri(uri, include_tables=include_tables)
    return db
