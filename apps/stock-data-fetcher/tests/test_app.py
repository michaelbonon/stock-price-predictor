"""Tests for app module"""
from unittest import TestCase
from unittest.mock import Mock, call, patch
import pytest

from datetime import date
from kafka3 import KafkaProducer
from kafka3.errors import KafkaTimeoutError
from src.app import create_producer, main

mock_stock_codes = ["XYZ"]


class TestCreateProducer(TestCase):
    """Tests for create_producer function"""

    @patch("src.app.KafkaProducer")
    def test_create_producer(self, mock_kafka_producer: Mock):
        """Successfully creates producer"""
        with self.assertLogs() as logs:
            # Act
            producer = create_producer("server_addr")

            # Assert
            self.assertEqual(
                logs.output,
                [
                    "INFO:root:Connecting to Kafka server at server_addr ...",
                    "INFO:root:Connected to Kafka server",
                ],
            )
            self.assertEqual(producer, mock_kafka_producer.return_value)
            mock_kafka_producer.assert_called_once_with(
                bootstrap_servers="server_addr", api_version=(7, 1, 3)
            )

    @patch("src.app.KafkaProducer")
    def test_create_producer_raises_exception(self, mock_kafka_producer: Mock):
        """Creating KafkaProducer raises exception"""
        # Arrange
        mock_kafka_producer.side_effect = Exception("Error")

        # Act
        # Assert
        with self.assertLogs() as logs:
            with self.assertRaises(ConnectionError):
                create_producer("server_addr")

            self.assertEqual(
                logs.output,
                [
                    "INFO:root:Connecting to Kafka server at server_addr ...",
                    "WARNING:root:Error connecting to Kafka server at server_addr",
                ],
            )


# Test cases for main
# - successfully send data via producer.send
# - no TOPIC environment variable raises RuntimeError
# - no SERVER_ADDR environment variable raises RuntimeError
# - scrape_stock_data raises RuntimeError
# - producer.send raises KafkaTimeoutError
# - producer.flush raises Exception
# - producer.close raises Exception


@patch("src.app.STOCK_CODES", mock_stock_codes)
class TestMain(TestCase):
    """Tests for main function"""

    @patch("src.app.json")
    @patch("src.app.scrape_stock_data")
    @patch("src.app.create_producer")
    @patch("src.app.os")
    def test_successful_send(
        self,
        mock_os: Mock,
        mock_create_producer: Mock,
        mock_scrape_stock_data: Mock,
        mock_json: Mock,
    ):
        """Test data is sent successfully data via producer.send"""
        # Arrange
        mock_os.environ = {"TOPIC": "topic", "SERVER_ADDR": "server_addr"}
        mock_producer = Mock(spec=KafkaProducer)
        mock_producer.send.return_value = None
        mock_create_producer.return_value = mock_producer
        mock_scrape_stock_data.return_value = "stock_data"
        mock_json.dumps.return_value = mock_json
        mock_json.encode.return_value = "encoded_json"

        with patch("src.app.date") as mock_date:
            mock_date.today.return_value = date(2022, 1, 1)

            with self.assertLogs() as logs:
                # Act
                main()

                # Assert
                expected_calls = [call("topic", "encoded_json")] * len(
                    mock_stock_codes
                )
                mock_producer.send.assert_has_calls(expected_calls)
                self.assertEqual(
                    logs.output,
                    [
                        "INFO:root:Sending stock data for 2022-01-01 ...",
                        "INFO:root:Fetching stock data for XYZ ...",
                        "INFO:root:Stock data fetched: stock_data",
                        "INFO:root:Sending stock data for XYZ ...",
                        "INFO:root:Sent stock data for XYZ",
                        "INFO:root:Connection to Kafka server closed",
                        "INFO:root:Done sending all stock data",
                    ],
                )

    @patch("src.app.os")
    def test_no_topic_env_var_raises_runtime_error(self, mock_os: Mock):
        """Test no TOPIC environment variable raises RuntimeError"""
        # Arrange
        mock_os.environ = {"SERVER_ADDR": "server_addr"}

        # Act
        # Assert
        with self.assertLogs(level="ERROR") as logs:
            with pytest.raises(SystemExit):
                main()

            self.assertIn(
                "CRITICAL:root:Required TOPIC environment variable not set",
                logs.output,
            )

    @patch("src.app.os")
    def test_no_server_addr_env_var_raises_runtime_error(self, mock_os: Mock):
        """Test no SERVER_ADDR environment variable raises RuntimeError"""
        # Arrange
        mock_os.environ = {"TOPIC": "topic"}

        # Act
        # Assert
        with self.assertLogs(level="ERROR") as logs:
            with pytest.raises(SystemExit):
                main()

            self.assertIn(
                "CRITICAL:root:Required SERVER_ADDR environment variable not set",
                logs.output,
            )

    @patch("src.app.date")
    @patch("src.app.os")
    @patch("src.app.create_producer")
    @patch("src.app.scrape_stock_data")
    def test_scrape_stock_data_raises_runtime_error(
        self,
        mock_scrape_stock_data: Mock,
        mock_create_producer: Mock,
        mock_os: Mock,
        mock_date: Mock,
    ):
        """Test scrape_stock_data raises RuntimeError"""
        # Arrange
        mock_os.environ = {"TOPIC": "topic", "SERVER_ADDR": "server_addr"}
        mock_create_producer.return_value = Mock(spec=KafkaProducer)
        mock_scrape_stock_data.side_effect = RuntimeError("Error")
        mock_date.today.return_value = date(2022, 1, 1)

        # Act
        with self.assertLogs(level="ERROR") as logs:
            main()

            # Assert
            self.assertTrue(
                any(
                    "ERROR:root:Error fetching stock data for XYZ" in log
                    for log in logs.output
                )
            )

    @patch("src.app.date")
    @patch("src.app.os")
    @patch("src.app.create_producer")
    @patch("src.app.scrape_stock_data")
    def test_producer_send_raises_kafka_timeout_error(
        self,
        mock_scrape_stock_data: Mock,
        mock_create_producer: Mock,
        mock_os: Mock,
        mock_date: Mock,
    ):
        """Test producer.send raises KafkaTimeoutError"""

        # Arrange
        mock_os.environ = {"TOPIC": "topic", "SERVER_ADDR": "server_addr"}
        mock_producer = Mock(spec=KafkaProducer)
        mock_producer.send.side_effect = KafkaTimeoutError("Error")
        mock_create_producer.return_value = mock_producer
        mock_scrape_stock_data.return_value = "stock_data"
        mock_date.today.return_value = date(2022, 1, 1)

        # Act
        with self.assertLogs(level="ERROR") as logs:
            main()

            # Assert
            self.assertTrue(
                any(
                    "ERROR:root:Error sending stock data for XYZ" in log
                    for log in logs.output
                )
            )

    @patch("src.app.date")
    @patch("src.app.os")
    @patch("src.app.create_producer")
    @patch("src.app.scrape_stock_data")
    def test_producer_flush_raises_exception(
        self,
        mock_scrape_stock_data: Mock,
        mock_create_producer: Mock,
        mock_os: Mock,
        mock_date: Mock,
    ):
        """Test producer.flush raises Exception"""

        # Arrange
        mock_os.environ = {"TOPIC": "topic", "SERVER_ADDR": "server_addr"}
        mock_producer = Mock(spec=KafkaProducer)
        mock_producer.flush.side_effect = KafkaTimeoutError("Error")
        mock_create_producer.return_value = mock_producer
        mock_scrape_stock_data.return_value = "stock_data"
        mock_date.today.return_value = date(2022, 1, 1)

        # Act
        with self.assertLogs(level="ERROR") as logs:
            main()

            # Assert
            self.assertTrue(
                any(
                    "ERROR:root:Failed to flush buffered records within timeout"
                    in log
                    for log in logs.output
                )
            )
