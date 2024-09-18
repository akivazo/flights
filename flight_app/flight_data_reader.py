import csv
from typing import List

class FlightDataReader:
    '''
    Read and write the data from the csv file
    '''
    def read_flights_data(self) -> List[List]:
        '''
        Return list of lists.
        Each list is made of [flight_id, arrival_time, departure_time, succcess_status=""]
        '''
        result = []
        with open(self.__input_csv_file, newline='') as f:
            csv_reader = csv.reader(f)
            # save the header line
            self.__header = next(csv_reader)
            for row in csv_reader:
                # add only if not empty
                if row:
                    result.append(row)
            return result

    def write_flights_data(self, flights: List[List]):
        '''
        Write the flights data into the output file 
        '''
        with open(self.__output_csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            #write header
            writer.writerow(self.__header)
            # Write the data to the CSV file
            writer.writerows(flights)

    def __init__(self, input_csv_file, output_csv_file= None):
        self.__input_csv_file = input_csv_file
        # if output file is None use the input file for output
        self.__output_csv_file = input_csv_file if output_csv_file is None else output_csv_file

    
    def get_data(self) -> List[List]:
        return self.read_flights_data()
