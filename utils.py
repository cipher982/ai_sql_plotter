import os


class MissingEnvironmentVariableError(Exception):
    pass


def load_sf_account() -> tuple:
    """
    Loads Snowflake connection parameters from environment variables or a `.env` file.

    Returns:
        A tuple in the form of (uri, openai_key).
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
        "OPENAI_API_KEY",
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
    return (uri, env_vars["OPENAI_API_KEY"])
