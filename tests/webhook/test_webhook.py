from unittest.mock import patch, MagicMock

with patch.dict(
    "os.environ",
    {"PK_PATH": "keys/private_key.pem", "PROJECT_ID": "123", "LOCAL_ENV": "true"},
):
    with patch("builtins.open", MagicMock(read_data="fake-key")):
        from src.webhook.webhook import (
            unpack_event,
            get_invoice_amount,
            execute_transfer,
            lambda_handler,
        )


class TestUnpackEvent:
    @patch("src.webhook.webhook.starkbank")
    def test_parses_event_content(self, mock_starkbank):
        mock_event = MagicMock()
        mock_starkbank.event.parse.return_value = mock_event

        result = unpack_event("{}", {"Digital-Signature": "test-signature"})

        mock_starkbank.event.parse.assert_called_once_with(
            content="{}", signature="test-signature"
        )
        assert result == mock_event


class TestGetInvoiceAmount:
    def test_returns_amount_for_invoice_subscription(self):
        mock_event = MagicMock()
        mock_event.subscription = "invoice"
        mock_event.log.invoice.amount = 10000

        result = get_invoice_amount(mock_event)

        assert result == 10000

    def test_returns_none_for_non_invoice_subscription(self):
        mock_event = MagicMock()
        mock_event.subscription = "other"

        result = get_invoice_amount(mock_event)

        assert result is None


class TestExecuteTransfer:
    def test_execute_transfer_calls_starkbank(self):
        with patch("src.webhook.webhook.starkbank") as mock_sb:
            mock_sb.transfer.create.return_value = [MagicMock()]

            execute_transfer(5000)

            mock_sb.transfer.create.assert_called_once()


class TestLambdaHandler:
    @patch("src.webhook.webhook.execute_transfer")
    @patch("src.webhook.webhook.get_invoice_amount")
    @patch("src.webhook.webhook.unpack_event")
    def test_returns_success_with_transfer(
        self, mock_unpack, mock_get_amount, mock_transfer
    ):
        mock_event = MagicMock()
        mock_unpack.return_value = mock_event
        mock_get_amount.return_value = 5000

        result = lambda_handler({"body": "{}", "headers": {}}, None)

        assert result["statusCode"] == 200
        assert "5000" in result["body"]
        mock_transfer.assert_called_once_with(5000)

    @patch("src.webhook.webhook.unpack_event")
    def test_returns_400_on_exception(self, mock_unpack):
        mock_unpack.side_effect = Exception("Invalid signature")

        result = lambda_handler({"body": "{}", "headers": {}}, None)

        assert result["statusCode"] == 400
        assert "error" in result["body"]
