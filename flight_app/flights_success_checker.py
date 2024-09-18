from .flight_data_reader import FlightDataReader
from datetime import datetime
import sys, os

class FlightSuccessChecker:
    '''
    For each flight update its status:
        The flight will defined as 'success' if:
            - the difference between the arrival and departure is greater or equal than 'min_minutes_delta' minutes.
            - There is no more than 'max_success' successed flights arrivals before this flight arrival.
        Otherwise the flight will defined as 'fail'.
    '''
    def __init__(self, flights_data, min_minutes_delta=180, max_success=20) -> None:
        self.__flight_data = flights_data
        self.__min_minutes_delta = min_minutes_delta
        self.__max_success = max_success

    def get_flights_with_success_status(self) -> list:
        # sort the flight by arrival
        sorted_flights = list(sorted(self.__flight_data, key=lambda flight_data: flight_data[1]))
        self.__update_status_by_min_time_delta(sorted_flights)
        self.__update_status_if_too_much_success(sorted_flights)
        return sorted_flights
    
    
    
        
    def __update_status_if_too_much_success(self, sorted_flights):
        # count the successed flights 
        success_count = 0
        for row in sorted_flights:
            if success_count >= self.__max_success:
                # if we already have 20 or more successed flights, all other flights should be mark as fail 
                row[3] = "fail"
                continue
            if row[3] == "success":
                success_count += 1

    def __get_minutes_delta(self, time1: str, time2: str):
        # return the time delta in minutes between 'time1' and 'time2' 
        format = "%H:%M"
        time1_dt = datetime.strptime(time1.strip(), format)
        time2_dt = datetime.strptime(time2.strip(), format)

        time_delta = time2_dt - time1_dt
        return time_delta.total_seconds() / 60
    
    def __update_status_by_min_time_delta(self, sorted_flights):
        for row in sorted_flights:
            arrival = row[1]
            departure = row[2]
            
            # time in minutes between arrival and departure
            time_delta = self.__get_minutes_delta(time1=arrival, time2=departure)

            if time_delta >= self.__min_minutes_delta:
                # The time between arrival and departure is greater or equal than 180 minutes so mark as success
                row[3] = "success"
            else:
                row[3] = "fail"
        

class FlightSuccessCheckerEntryPoint:
    '''
    A wrapper class to retrieve the data from the file and write after proccessing
    '''
    def __init__(self, input_csv_file, output_csv_file):
        self.__data_reader = FlightDataReader(input_csv_file, output_csv_file)
    
    def run(self):
        flights_data = self.__data_reader.get_data()

        flights_status_checker = FlightSuccessChecker(flights_data=flights_data)
        flights_data = flights_status_checker.get_flights_with_success_status()

        self.__data_reader.write_flights_data(flights=flights_data)


    
