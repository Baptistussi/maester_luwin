import os

os.environ["PROJECT_ID"] = "123"

from unittest.mock import MagicMock
import starkbank

mock_project = MagicMock()
mock_project.environment = "sandbox"
mock_project.id = "123"
starkbank.Project = MagicMock(return_value=mock_project)
starkbank.user = mock_project
starkbank.Invoice = MagicMock

from src.cronjob.add_invoices import generate_invoices


def test_generate_invoices_count():
    invoices = generate_invoices()
    assert 8 <= len(invoices) <= 12
