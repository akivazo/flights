from ...flight_app import flight_rest_api
import pytest
import json

flight_rest_api.data_file = r"tests\flight_rest_api\flight_data_with_status.csv"


@pytest.fixture
def client():
    flight_rest_api.flight_app.config['TESTING'] = True
    with flight_rest_api.flight_app.test_client() as client:
        yield client

def test_update_and_get_flight_data(client):
    # Update flights data
    new_flights = [
        ["1", "10:00", "12:00"],
        ["2", "13:00", "15:00"]
    ]
    response = client.post('/flights', json=new_flights)
    assert response.status_code == 200
    assert 'Flights updated successfully' in response.data.decode()

    # Verify the first flight data
    response = client.get('/flights/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == "1"
    assert data['arrival'] == "10:00"
    assert data['departure'] == "12:00"
    assert 'success' in data

    # Verify the second flight data
    response = client.get('/flights/2')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == "2"
    assert data['arrival'] == "13:00"
    assert data['departure'] == "15:00"
    assert 'success' in data

def test_update_flights_invalid_json(client):
    response = client.post('/flights', data="Invalid JSON")
    assert response.status_code == 400
    assert 'Invalid JSON data' in response.data.decode()
