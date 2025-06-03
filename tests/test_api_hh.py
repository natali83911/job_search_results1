from unittest.mock import Mock, patch

import pytest

from src.api_hh import HeadHunterAPI


def test_connect_success(api):
    with patch("requests.Session.get") as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = api._connect()
        mock_get.assert_called_once_with(url=api._HeadHunterAPI__base_url, headers=api._HeadHunterAPI__headers)
        assert response == mock_response


def test_connect_failure():
    api = HeadHunterAPI()
    with patch("requests.Session") as MockSession:
        mock_session = MockSession.return_value
        mock_session.get.side_effect = ConnectionError("Connection error")

        with pytest.raises(ConnectionError):
            api._connect()


def test_get_vacancies_success(api):
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"id": 1, "name": "Test"}]}
        mock_get.return_value = mock_response

        vacancies = api.get_vacancies(keyword="python", per_page=5, area=1)
        mock_get.assert_called_once()
        assert isinstance(vacancies, list)
        assert vacancies[0]["name"] == "Test"


def test_get_vacancies_failure(api):
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with pytest.raises(ConnectionError):
            api.get_vacancies(keyword="python")
