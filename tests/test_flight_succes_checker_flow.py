import pytest, csv
import filecmp
import os
from ..flight_app.flights_success_checker import FlightSuccessCheckerEntryPoint

def test_full_flow():
    before_csv_file = r"tests\flight_data_no_status.csv"

    after_csv_file = r"tests\flight_data_with_status.csv"

    expected_after_csv_file = r"tests\expected_flight_data_with_status.csv"

    if os.path.exists(after_csv_file):
        # freash start
        os.remove(after_csv_file)
    

    FlightSuccessCheckerEntryPoint(input_csv_file=before_csv_file, output_csv_file=after_csv_file).run()

    assert filecmp.cmp(after_csv_file, expected_after_csv_file)

    