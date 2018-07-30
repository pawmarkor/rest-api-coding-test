from flask import url_for


def test_holiday_offers_url(app):
    assert url_for('holiday-offers') == '/holiday_offers'


def test_holiday_offers_endpoint_get_only(client):
    assert client.get(url_for('holiday-offers')).status_code == 200
    assert client.post(url_for('holiday-offers')).status_code == 405
    assert client.put(url_for('holiday-offers')).status_code == 405
    assert client.patch(url_for('holiday-offers')).status_code == 405
