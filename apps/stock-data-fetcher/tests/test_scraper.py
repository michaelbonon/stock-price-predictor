"""Tests for scraper module"""
from unittest import TestCase
from unittest.mock import Mock, patch

import pytest
from bs4 import BeautifulSoup
from requests import HTTPError, JSONDecodeError, Response
from src.scraper import (
    fetch_company_id,
    fetch_stock_data_soup,
    get_close,
    get_high,
    get_low,
    get_open,
    get_volume,
    scrape_stock_data,
)


class TestGetClose(TestCase):
    """Tests for get_close function"""

    @patch("src.scraper.locale")
    def test_return_closing_price(self, mock_locale: Mock):
        """Test get_close function correctly parses the closing price"""
        # arrange
        mock_locale.atof.return_value = 1000.0
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = "1,000.00"

        # act
        close = get_close(mock_soup)

        # assert
        assert close == 1000.0

    def test_soup_find_returns_none(self):
        """Test get_close function raises RuntimeError when soup.find returns
        None"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = None

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_close(mock_soup)

    def test_soup_find_next_sibling_returns_none(self):
        """Test get_close function raises RuntimeError when
        soup.find_next_sibling returns None"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = None

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_close(mock_soup)

    def test_soup_text_is_empty_string(self):
        """Test get_close function returns 'N/A' when soup.text.strip() is an
        empty string"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = ""

        # act
        close = get_close(mock_soup)

        # assert
        assert close == "N/A"

    def test_soup_text_is_not_a_valid_float(self):
        """Test get_close function raises RuntimeError when soup.text.strip()
        is not a valid float"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = "abc"

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_close(mock_soup)


class TestGetOpen(TestCase):
    """Tests for get_open function"""

    @patch("src.scraper.locale")
    def test_return_opening_price(self, mock_locale: Mock):
        """Test get_open function correctly parses the opening price"""
        # arrange
        mock_locale.atof.return_value = 1000.0
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = "1,000.00"

        # act
        open_price = get_open(mock_soup)

        # assert
        assert open_price == 1000.0

    def test_soup_find_returns_none(self):
        """Test get_open function raises RuntimeError when soup.find returns
        None"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = None

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_open(mock_soup)

    def test_soup_find_next_sibling_returns_none(self):
        """Test get_open function raises RuntimeError when
        soup.find_next_sibling returns None"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = None

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_open(mock_soup)

    def test_soup_text_is_empty_string(self):
        """Test get_open function returns 'N/A' when soup.text.strip() is an
        empty string"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = ""

        # act
        open_price = get_open(mock_soup)

        # assert
        assert open_price == "N/A"

    def test_soup_text_is_not_a_valid_float(self):
        """Test get_open function raises RuntimeError when soup.text.strip()
        is not a valid float"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = "abc"

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_open(mock_soup)


class TestGetHigh(TestCase):
    """Tests for get_high function"""

    @patch("src.scraper.locale")
    def test_return_high_price(self, mock_locale: Mock):
        """Test get_high function correctly parses the high price"""
        # arrange
        mock_locale.atof.return_value = 1000.0
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = "1,000.00"

        # act
        high = get_high(mock_soup)

        # assert
        assert high == 1000.0

    def test_soup_find_returns_none(self):
        """Test get_high function raises RuntimeError when soup.find returns
        None"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = None

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_high(mock_soup)

    def test_soup_find_next_sibling_returns_none(self):
        """Test get_high function raises RuntimeError when
        soup.find_next_sibling returns None"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = None

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_high(mock_soup)

    def test_soup_text_is_empty_string(self):
        """Test get_high function returns 'N/A' when soup.text.strip() is an
        empty string"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = ""

        # act
        high = get_high(mock_soup)

        # assert
        assert high == "N/A"

    def test_soup_text_is_not_a_valid_float(self):
        """Test get_high function raises RuntimeError when soup.text.strip()
        is not a valid float"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = "abc"

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_high(mock_soup)


class TestGetLow(TestCase):
    """Tests for get_low function"""

    @patch("src.scraper.locale")
    def test_return_low_price(self, mock_locale: Mock):
        """Test get_low function correctly parses the low price"""
        # arrange
        mock_locale.atof.return_value = 1000.0
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = "1,000.00"

        # act
        low = get_low(mock_soup)

        # assert
        assert low == 1000.0

    def test_soup_find_returns_none(self):
        """Test get_low function raises RuntimeError when soup.find returns
        None"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = None

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_low(mock_soup)

    def test_soup_find_next_sibling_returns_none(self):
        """Test get_low function raises RuntimeError when
        soup.find_next_sibling returns None"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = None

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_low(mock_soup)

    def test_soup_text_is_empty_string(self):
        """Test get_low function returns 'N/A' when soup.text.strip() is an
        empty string"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = ""

        # act
        low = get_low(mock_soup)

        # assert
        assert low == "N/A"

    def test_soup_text_is_not_a_valid_float(self):
        """Test get_low function raises RuntimeError when soup.text.strip()
        is not a valid float"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = "abc"

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_low(mock_soup)


class TestGetVolume(TestCase):
    """Tests for get_volume function"""

    @patch("src.scraper.locale")
    def test_return_volume(self, mock_locale: Mock):
        """Test get_volume function correctly parses the volume"""
        # arrange
        mock_locale.atoi.return_value = 1000
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = "1,000"

        # act
        volume = get_volume(mock_soup)

        # assert
        assert volume == 1000

    def test_soup_find_returns_none(self):
        """Test get_volume function raises RuntimeError when soup.find returns
        None"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = None

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_volume(mock_soup)

    def test_soup_find_next_sibling_returns_none(self):
        """Test get_volume function raises RuntimeError when
        soup.find_next_sibling returns None"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = None

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_volume(mock_soup)

    def test_soup_text_is_empty_string(self):
        """Test get_volume function returns 'N/A' when soup.text.strip() is an
        empty string"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = ""

        # act
        volume = get_volume(mock_soup)

        # assert
        assert volume == "N/A"

    def test_soup_text_is_not_a_valid_int(self):
        """Test get_volume function raises RuntimeError when soup.text.strip()
        is not a valid int"""
        # arrange
        mock_soup = Mock(name="soup", spec=BeautifulSoup)
        mock_soup.find.return_value = mock_soup
        mock_soup.find_next_sibling.return_value = mock_soup
        mock_soup.text = "abc"

        # act
        # assert
        with pytest.raises(RuntimeError):
            get_volume(mock_soup)


class TestFetchCompanyId(TestCase):
    """Tests for fetch_company_id function"""

    @patch("src.scraper.requests")
    def test_return_company_id(self, mock_requests: Mock):
        """Test fetch_company_id function returns company id"""
        # arrange
        mock_response = Mock(name="response", spec=Response)
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [{"cmpyId": 1234}]
        mock_requests.get.return_value = mock_response

        # act
        company_id = fetch_company_id("AAPL")

        # assert
        assert company_id == 1234

    @patch("src.scraper.requests")
    def test_raise_for_status_raises_http_error(self, mock_requests: Mock):
        """Test fetch_company_id function raises RuntimeError when
        response.raise_for_status() raises an HTTPError"""
        # arrange
        mock_response = Mock(name="response", spec=Response)
        mock_response.raise_for_status.side_effect = HTTPError()
        mock_requests.get.return_value = mock_response

        # act
        # assert
        with pytest.raises(RuntimeError):
            fetch_company_id("AAPL")

    @patch("src.scraper.requests")
    def test_json_raises_json_decode_error(self, mock_requests: Mock):
        """Test fetch_company_id function raises RuntimeError when
        response.json()[0]["cmpyId"] raises a JSONDecodeError"""
        # arrange
        mock_response = Mock(name="response", spec=Response)
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = JSONDecodeError("", "", 0)
        mock_requests.get.return_value = mock_response

        # act
        # assert
        with pytest.raises(RuntimeError):
            fetch_company_id("AAPL")


class TestFetchStockDataSoup(TestCase):
    """Tests for fetch_stock_data_soup function"""

    @patch("src.scraper.BeautifulSoup")
    @patch("src.scraper.requests")
    def test_return_beautiful_soup_object(
        self, mock_requests: Mock, mock_beautiful_soup: Mock
    ):
        """Test fetch_stock_data_soup function returns BeautifulSoup object"""
        # arrange
        mock_response = Mock(name="response", spec=Response)
        mock_response.raise_for_status.return_value = None
        mock_response.text = "abc"
        mock_requests.get.return_value = mock_response

        # act
        soup = fetch_stock_data_soup(1234)

        # assert
        assert soup == mock_beautiful_soup.return_value

    @patch("src.scraper.requests")
    def test_raise_for_status_raises_http_error(self, mock_requests: Mock):
        """Test fetch_stock_data_soup function raises RuntimeError when
        response.raise_for_status() raises an HTTPError"""
        # arrange
        mock_response = Mock(name="response", spec=Response)
        mock_response.raise_for_status.side_effect = HTTPError()
        mock_requests.get.return_value = mock_response

        # act
        # assert
        with pytest.raises(RuntimeError):
            fetch_stock_data_soup(1234)

    @patch("src.scraper.BeautifulSoup")
    @patch("src.scraper.requests")
    def test_beautiful_soup_raises_error(
        self, mock_requests: Mock, mock_beautiful_soup: Mock
    ):
        """Test fetch_stock_data_soup function raises RuntimeError when
        BeautifulSoup(response.text, "html.parser") raises an error"""
        # arrange
        mock_response = Mock(name="response", spec=Response)
        mock_response.raise_for_status.return_value = None
        mock_response.text = "abc"
        mock_requests.get.return_value = mock_response
        mock_beautiful_soup.side_effect = Exception()

        # act
        # assert
        with pytest.raises(RuntimeError):
            fetch_stock_data_soup(1234)


class TestScrapeStockData(TestCase):
    """Tests for scrape_stock_data function"""

    @patch("src.scraper.get_volume")
    @patch("src.scraper.get_low")
    @patch("src.scraper.get_high")
    @patch("src.scraper.get_open")
    @patch("src.scraper.get_close")
    @patch("src.scraper.fetch_stock_data_soup")
    @patch("src.scraper.fetch_company_id")
    def test_return_stock_data_object(
        self,
        mock_fetch_company_id: Mock,
        mock_fetch_stock_data_soup: Mock,
        mock_get_close: Mock,
        mock_get_open: Mock,
        mock_get_high: Mock,
        mock_get_low: Mock,
        mock_get_volume: Mock,
    ):
        """Test scrape_stock_data function returns StockData object"""
        # arrange
        mock_fetch_company_id.return_value = 1234
        mock_fetch_stock_data_soup.return_value = "soup"
        mock_get_close.return_value = 1.0
        mock_get_open.return_value = 2.0
        mock_get_high.return_value = 3.0
        mock_get_low.return_value = 4.0
        mock_get_volume.return_value = 5

        # act
        stock_data = scrape_stock_data("AAPL")

        # assert
        assert stock_data == {
            "stock": "AAPL",
            "close": 1.0,
            "open": 2.0,
            "high": 3.0,
            "low": 4.0,
            "volume": 5,
        }

    @patch("src.scraper.fetch_company_id")
    def test_fetch_company_id_raises_error(self, mock_fetch_company_id: Mock):
        """Test scrape_stock_data function raises RuntimeError when
        fetch_company_id(stock_symbol) raises an error"""
        # arrange
        mock_fetch_company_id.side_effect = RuntimeError()

        # act
        # assert
        with pytest.raises(RuntimeError):
            scrape_stock_data("AAPL")

    @patch("src.scraper.fetch_stock_data_soup")
    @patch("src.scraper.fetch_company_id")
    def test_fetch_stock_data_soup_raises_error(
        self, mock_fetch_company_id: Mock, mock_fetch_stock_data_soup: Mock
    ):
        """Test scrape_stock_data function raises RuntimeError when
        fetch_stock_data_soup(company_id) raises an error"""
        # arrange
        mock_fetch_company_id.return_value = 1234
        mock_fetch_stock_data_soup.side_effect = RuntimeError()

        # act
        # assert
        with pytest.raises(RuntimeError):
            scrape_stock_data("AAPL")

    @patch("src.scraper.get_close")
    @patch("src.scraper.fetch_stock_data_soup")
    @patch("src.scraper.fetch_company_id")
    def test_get_close_raises_error(
        self,
        mock_fetch_company_id: Mock,
        mock_fetch_stock_data_soup: Mock,
        mock_get_close: Mock,
    ):
        """Test scrape_stock_data function raises RuntimeError when
        get_close(soup) raises an error"""
        # arrange
        mock_fetch_company_id.return_value = 1234
        mock_fetch_stock_data_soup.return_value = "soup"
        mock_get_close.side_effect = RuntimeError()

        # act
        # assert
        with pytest.raises(RuntimeError):
            scrape_stock_data("AAPL")

    @patch("src.scraper.get_open")
    @patch("src.scraper.get_close")
    @patch("src.scraper.fetch_stock_data_soup")
    @patch("src.scraper.fetch_company_id")
    def test_get_open_raises_error(
        self,
        mock_fetch_company_id: Mock,
        mock_fetch_stock_data_soup: Mock,
        mock_get_close: Mock,
        mock_get_open: Mock,
    ):
        """Test scrape_stock_data function raises RuntimeError when
        get_open(soup) raises an error"""
        # arrange
        mock_fetch_company_id.return_value = 1234
        mock_fetch_stock_data_soup.return_value = "soup"
        mock_get_close.return_value = 1.0
        mock_get_open.side_effect = RuntimeError()

        # act
        # assert
        with pytest.raises(RuntimeError):
            scrape_stock_data("AAPL")

    @patch("src.scraper.get_high")
    @patch("src.scraper.get_open")
    @patch("src.scraper.get_close")
    @patch("src.scraper.fetch_stock_data_soup")
    @patch("src.scraper.fetch_company_id")
    def test_get_high_raises_error(
        self,
        mock_fetch_company_id: Mock,
        mock_fetch_stock_data_soup: Mock,
        mock_get_close: Mock,
        mock_get_open: Mock,
        mock_get_high: Mock,
    ):
        """Test scrape_stock_data function raises RuntimeError when
        get_high(soup) raises an error"""
        # arrange
        mock_fetch_company_id.return_value = 1234
        mock_fetch_stock_data_soup.return_value = "soup"
        mock_get_close.return_value = 1.0
        mock_get_open.return_value = 2.0
        mock_get_high.side_effect = RuntimeError()

        # act
        # assert
        with pytest.raises(RuntimeError):
            scrape_stock_data("AAPL")

    @patch("src.scraper.get_low")
    @patch("src.scraper.get_high")
    @patch("src.scraper.get_open")
    @patch("src.scraper.get_close")
    @patch("src.scraper.fetch_stock_data_soup")
    @patch("src.scraper.fetch_company_id")
    def test_get_low_raises_error(
        self,
        mock_fetch_company_id: Mock,
        mock_fetch_stock_data_soup: Mock,
        mock_get_close: Mock,
        mock_get_open: Mock,
        mock_get_high: Mock,
        mock_get_low: Mock,
    ):
        """Test scrape_stock_data function raises RuntimeError when
        get_low(soup) raises an error"""
        # arrange
        mock_fetch_company_id.return_value = 1234
        mock_fetch_stock_data_soup.return_value = "soup"
        mock_get_close.return_value = 1.0
        mock_get_open.return_value = 2.0
        mock_get_high.return_value = 3.0
        mock_get_low.side_effect = RuntimeError()

        # act
        # assert
        with pytest.raises(RuntimeError):
            scrape_stock_data("AAPL")

    @patch("src.scraper.get_volume")
    @patch("src.scraper.get_low")
    @patch("src.scraper.get_high")
    @patch("src.scraper.get_open")
    @patch("src.scraper.get_close")
    @patch("src.scraper.fetch_stock_data_soup")
    @patch("src.scraper.fetch_company_id")
    def test_get_volume_raises_error(
        self,
        mock_fetch_company_id: Mock,
        mock_fetch_stock_data_soup: Mock,
        mock_get_close: Mock,
        mock_get_open: Mock,
        mock_get_high: Mock,
        mock_get_low: Mock,
        mock_get_volume: Mock,
    ):
        """Test scrape_stock_data function raises RuntimeError when
        get_volume(soup) raises an error"""
        # arrange
        mock_fetch_company_id.return_value = 1234
        mock_fetch_stock_data_soup.return_value = "soup"
        mock_get_close.return_value = 1.0
        mock_get_open.return_value = 2.0
        mock_get_high.return_value = 3.0
        mock_get_low.return_value = 4.0
        mock_get_volume.side_effect = RuntimeError()

        # act
        # assert
        with pytest.raises(RuntimeError):
            scrape_stock_data("AAPL")
