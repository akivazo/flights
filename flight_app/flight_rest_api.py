from flask import Flask, request, jsonify
from .flight_data_reader import FlightDataReader
from .flights_success_checker import FlightSuccessChecker
import sys

flight_app = Flask(__name__)
data_reader = None

def init_app_data_file(data_file):
    global flight_app, data_reader
    data_reader = FlightDataReader(data_file)

@flight_app.route("/flights/<flight_id>", methods=["GET"])
def get_flight_data(flight_id):
    # Get existing flights
    flights_data = data_reader.get_data()
    # Search for flight that matches the id and return it
    for flight in flights_data:
        if flight_id == flight[0]:
            data = {
                "id": flight[0],
                "arrival": flight[1],
                "departure": flight[2],
                "success": flight[3]
            }
            return jsonify(data), 200
    # If not found, return 404
    return jsonify({"error": f"Flight id: {flight_id} was not found"}), 404

@flight_app.route("/flights", methods=["POST"])
def update_flights():
    """
    The JSON is expected to be a list of lists.
    Each list represents a flight and is composed of [flight_id, arrival (in the format %H:%M), departure (in the format %H:%M)].
    """
    # Get existing flights
    flights_data = data_reader.get_data()
    if request.is_json:
        json_data = request.get_json()
        # Add the input flights
        flights_data.extend(json_data)
        # Add the 'success' field
        for flight_data in flights_data:
            flight_data.append("")
        success_checker = FlightSuccessChecker(flights_data)
        # Update the success field
        checked_flights = success_checker.get_flights_with_success_status()
        data_reader.write_flights_data(checked_flights)
        return jsonify({"message": "Flights updated successfully"}), 200
    else:
        return jsonify({"error": "Invalid JSON data"}), 400

if __name__ == '__main__':
    data_file = r"flight_app/flights_data.csv"
    init_app_data_file(data_file)
    flight_app.run(debug=True)
