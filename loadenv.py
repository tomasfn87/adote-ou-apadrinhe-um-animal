from os import environ as env

def load_env_file():
    with open(".env", "r") as env_file:
        for line in env_file:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                env[key] = value