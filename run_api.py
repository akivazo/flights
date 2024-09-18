from flight_app.flight_rest_api import flight_app, init_app_data_file
from waitress import serve

if __name__ == '__main__':
    # use waitress for production
    init_app_data_file(r"flight_app/flights_data.csv")
    serve(flight_app, host="127.0.0.1", port=5000)