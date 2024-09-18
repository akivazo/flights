from ...flight_app.flight_rest_api import init_app_data_file, flight_app
from flask.testing import FlaskClient
import pytest
import json



def init_flight_data_file(file):
    # init the flight data file for a freash start
    with open(file, mode="w") as f:
        f.write("Flight ID, Arrival, Departure , success")

@pytest.fixture
def client():
    test_data_file = r"tests\flight_rest_api\flight_data_with_status.csv"
    init_flight_data_file(test_data_file) 
    init_app_data_file(test_data_file) # set the data file to use
    flight_app.config['TESTING'] = True
    with flight_app.test_client() as client:
        yield client

def test_flight_not_found(client: FlaskClient):
    response = client.get('/flights/1')
    assert response.status_code == 404
    assert 'Flight id: 1 was not found' in response.data.decode()

def test_update_and_get_flight_data(client: FlaskClient):
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

def test_update_flights_invalid_json(client: FlaskClient):
    response = client.post('/flights', data="Invalid JSON")
    assert response.status_code == 400
    assert 'Invalid JSON data' in response.data.decode()
