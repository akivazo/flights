from flight_app.flights_success_checker import FlightSuccessCheckerEntryPoint
import sys

if __name__ == "__main__":
    input_csv_file = sys.argv[1]
    output_csv_file = None
    if len(sys.argv) == 3:
        # there is also output file
        output_csv_file = sys.argv[2]
    FlightSuccessCheckerEntryPoint(input_csv_file=input_csv_file, output_csv_file=output_csv_file).run()