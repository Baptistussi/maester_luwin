import os
import boto3

LOCAL_ENV = os.getenv("LOCAL_ENV", False)
PK_PATH = os.getenv("PK_PATH")
PROJECT_ID = os.getenv("PROJECT_ID")

if not PROJECT_ID:
    raise Exception("Necessary env var PROJECT_ID not set.")

if LOCAL_ENV:
    if not PK_PATH:
        raise Exception("Necessary env var for LOCAL_ENV PK_PATH not set.")

    with open(PK_PATH, "r") as key_file:
        PRIVATE_KEY_CONTENT = key_file.read()

        if not PRIVATE_KEY_CONTENT:
            raise Exception(f"Failed to load key from {PK_PATH}")
else:
    SSM_PARAM_NAME = os.getenv("SSM_PARAM_NAME", "/starkbank/private-key")

    ssm = boto3.client("ssm", region_name=os.getenv("AWS_REGION", "us-east-1"))
    response = ssm.get_parameter(Name=SSM_PARAM_NAME, WithDecryption=True)
    PRIVATE_KEY_CONTENT = response["Parameter"]["Value"]

    if not PRIVATE_KEY_CONTENT:
        raise Exception(f"Failed to load key from SSM: {SSM_PARAM_NAME}")
