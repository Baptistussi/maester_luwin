import os

PK_PATH = os.getenv("PK_PATH")
PROJECT_ID = os.getenv("PROJECT_ID")

if not PK_PATH:
    raise Exception("Necessary env var PK_PATH not set.")

if not PROJECT_ID:
    raise Exception("Necessary env var PROJECT_ID not set.")

PRIVATE_KEY_CONTENT = None
with open(PK_PATH, "r") as key_file:
    PRIVATE_KEY_CONTENT = key_file.read()


if not PRIVATE_KEY_CONTENT:
    raise Exception(f"Failed to load key from file: {PK_PATH}")
