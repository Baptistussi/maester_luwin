import json
import random
from datetime import datetime, timedelta, timezone
import starkbank

from src.shared.config import PRIVATE_KEY_CONTENT, PROJECT_ID
from src.cronjob.fake_info import fake_amount, fake_full_name, generate_cpf


def set_project() -> starkbank.Project:
    project = starkbank.Project(
        environment="sandbox", id=PROJECT_ID, private_key=PRIVATE_KEY_CONTENT
    )
    starkbank.user = project


def generate_invoices() -> list[starkbank.Invoice]:
    number_of_invoices = random.randint(8, 12)
    invoices = []
    for _ in range(number_of_invoices):
        invoice = starkbank.Invoice(
            amount=fake_amount(),
            name=fake_full_name(),
            tax_id=generate_cpf(),
            due=datetime.now(timezone.utc) + timedelta(hours=1),
            expiration=timedelta(hours=3).total_seconds(),
            fine=5,  # 5%
            interest=2.5,  # 2.5% per month
            tags=["immediate"],
        )
        invoices.append(invoice)
    return invoices


def lambda_handler(event, context):
    print("Invocation event:", event)

    set_project()
    print("Starkbank project set")

    invoices = generate_invoices()
    print(f"Generated {len(invoices)} invoices")

    invoices_result = starkbank.invoice.create(invoices)
    return {
        "statusCode": 200,
        "body": json.dumps(f"Created {len(invoices_result)} invoices"),
    }
