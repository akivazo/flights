import csv
from typing import List

class FlightDataReader:
    def read_flights_data(self):
        with open(self.__input_csv_file, newline='') as f:
            csv_reader = csv.reader(f)
            # save the header line
            self.__header = next(csv_reader)
            return list(csv_reader)

    def write_flights_data(self, flights):
        with open(self.__output_csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            #write header
            writer.writerow(self.__header)
            # Write the data to the CSV file
            writer.writerows(flights)

    def __init__(self, input_csv_file, output_csv_file= None):
        self.__input_csv_file = input_csv_file
        self.__output_csv_file = input_csv_file if output_csv_file is None else output_csv_file

    
    def get_data(self) -> List[List]:
        return self.read_flights_data()
