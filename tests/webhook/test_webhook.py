import os

os.environ["LOCAL_ENV"] = "true"
os.environ["PK_PATH"] = "keys/privateKey.pem"
os.environ["PROJECT_ID"] = "123"

from unittest.mock import MagicMock
import starkbank

mock_project = MagicMock()
mock_project.environment = "sandbox"
mock_project.id = "123"
starkbank.Project = MagicMock(return_value=mock_project)
starkbank.user = mock_project
starkbank.event = MagicMock()
starkbank.Transfer = MagicMock()

from src.webhook.webhook import get_invoice_amount, unpack_event, generate_transfer


def test_unpack_event():
    mock_event = MagicMock()
    starkbank.event.parse.return_value = mock_event

    result = unpack_event("{}", {"Digital-Signature": "test-sig"})

    starkbank.event.parse.assert_called_once_with(content="{}", signature="test-sig")
    assert result == mock_event


def test_generate_transfer():
    transfers = generate_transfer(5000)

    assert len(transfers) == 1
    starkbank.Transfer.assert_called_once_with(
        amount=5000,
        tax_id="20.018.183/0001-80",
        name="Stark Bank S.A.",
        bank_code="20018183",
        branch_code="0001",
        account_number="6341320293482496",
        tags=["webhook transfer"],
        account_type="payment",
    )


def test_get_invoice_amount_with_invoice():
    event = MagicMock()
    event.subscription = "invoice"
    event.log.invoice.amount = 5000
    assert get_invoice_amount(event) == 5000


def test_get_invoice_amount_without_invoice():
    event = MagicMock()
    event.subscription = "other"
    assert get_invoice_amount(event) is None
