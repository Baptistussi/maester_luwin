from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

with patch.dict("os.environ", {"PK_PATH": "keys/private_key.pem", "PROJECT_ID": "123"}):
    with patch("builtins.open", MagicMock()):
        with patch("src.shared.config.PRIVATE_KEY_CONTENT", "fake-key"):
            from src.cronjob.add_invoices import generate_invoices, lambda_handler


class TestGenerateInvoices:
    def test_generates_between_8_and_12_invoices(self):
        invoices = generate_invoices()
        assert 8 <= len(invoices) <= 12

    def test_invoice_has_required_fields(self):
        invoices = generate_invoices()
        for invoice in invoices:
            assert invoice.amount > 0
            assert invoice.name is not None
            assert invoice.tax_id is not None
            assert invoice.due > datetime.now(timezone.utc)
            assert invoice.expiration == 10800  # 3 hours in seconds
            assert invoice.fine == 5
            assert invoice.interest == 2.5
            assert "immediate" in invoice.tags


class TestLambdaHandler:
    @patch("src.cronjob.add_invoices.starkbank")
    def test_returns_success_status(self, mock_starkbank):
        mock_starkbank.invoice.create.return_value = [MagicMock(), MagicMock()]

        result = lambda_handler({}, None)

        assert result["statusCode"] == 200

    @patch("src.cronjob.add_invoices.starkbank")
    def test_creates_invoices_via_starkbank(self, mock_starkbank):
        mock_starkbank.invoice.create.return_value = []

        lambda_handler({}, None)

        mock_starkbank.invoice.create.assert_called_once()
