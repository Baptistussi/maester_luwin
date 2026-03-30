import json
import starkbank
from src.shared.config import PRIVATE_KEY_CONTENT, PROJECT_ID


def set_project() -> starkbank.Project:
    project = starkbank.Project(
        environment="sandbox", id=PROJECT_ID, private_key=PRIVATE_KEY_CONTENT
    )
    starkbank.user = project


def unpack_event(body, headers):
    return starkbank.event.parse(
        content=body,
        signature=headers.get("Digital-Signature"),
    )


def get_invoice_amount(event):
    if event.subscription == "invoice":
        return event.log.invoice.amount


def generate_transfer(amount) -> list[starkbank.Transfer]:
    transfers = [
        starkbank.Transfer(
            amount=amount,
            tax_id="20.018.183/0001-80",
            name="Stark Bank S.A.",
            bank_code="20018183",
            branch_code="0001",
            account_number="6341320293482496",
            tags=["webhook transfer"],
            account_type="payment",
        )
    ]
    return transfers


def lambda_handler(event, context):
    print("Invocation event:", event)

    set_project()
    print("Starkbank project set")
    try:
        body = event.get("body", "{}")
        headers = event.get("headers", {})

        event = unpack_event(body, headers)
        amount = get_invoice_amount(event)

        if not amount:
            raise Exception("Couldn't get invoice amount from the data received.")

        transfers = generate_transfer(amount)
        print(f"Generated transfer for {amount}")

        starkbank.transfer.create(transfers)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": f"Transfered {amount}"}),
        }

    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"error": str(e)})}
