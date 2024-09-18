import pytest
from ...flight_app.flights_success_checker import FlightSuccessChecker

def get_flights_status_checker(data):
    return FlightSuccessChecker(flights_data=data)

def test_no_flights():
    flights_status_checker  = get_flights_status_checker(data=[])
    res = flights_status_checker.get_flights_with_success_status()

    assert res == []

def test_all_success():
    flights_status_checker = get_flights_status_checker(data=[
        ["id3", "16:00", "20:31", ""],
        ["id1", "00:00", "03:00", ""],
        ["id2", "01:30", "05:00", ""],
        
    ])

    res = flights_status_checker.get_flights_with_success_status()

    # assert all success and sorted by arrival
    assert res == [
        ["id1", "00:00", "03:00", "success"],
        ["id2", "01:30", "05:00", "success"],
        ["id3", "16:00", "20:31", "success"]
    ]


def test_short_time_delta():
    flights_status_checker = get_flights_status_checker(data=[
        ["id3", "16:00", "16:01", ""],
        ["id1", "00:00", "02:59", ""],
        ["id2", "01:30", "05:00", ""],
        ["id4", "15:30", "21:00", ""],
        
    ])

    res = flights_status_checker.get_flights_with_success_status()

    # assert correct status and sorted by arrival
    assert res == [
        ["id1", "00:00", "02:59", "fail"],
        ["id2", "01:30", "05:00", "success"],
        ["id4", "15:30", "21:00", "success"],
        ["id3", "16:00", "16:01", "fail"]
    ]

def test_too_much_success():
    flights_status_checker = get_flights_status_checker(data=[
        ["id1", "00:00", "03:01", ""],
        ["id2", "01:00", "04:01", ""],
        ["id3", "02:00", "05:01", ""],
        ["id4", "03:00", "03:01", ""],
        ["id5", "04:00", "07:01", ""],
        ["id6", "05:00", "08:01", ""],
        ["id7", "06:00", "09:01", ""],
        ["id8", "07:00", "10:01", ""],
        ["id9", "08:00", "11:01", ""],
        ["id10", "09:00", "12:01", ""],
        ["id11", "10:00", "13:01", ""],
        ["id12", "11:00", "14:01", ""],
        ["id13", "12:00", "15:01", ""],
        ["id14", "13:00", "16:01", ""],
        ["id15", "14:00", "17:01", ""],
        ["id16", "15:00", "18:01", ""],
        ["id17", "16:00", "19:01", ""],
        ["id18", "17:00", "20:01", ""],
        ["id19", "18:00", "21:01", ""],
        ["id20", "19:00", "22:01", ""],
        ["id21", "20:00", "23:01", ""],
        ["id22", "20:05", "23:10", ""],
    ])

    res = flights_status_checker.get_flights_with_success_status()

    assert res ==   [
        ["id1", "00:00", "03:01", "success"],
        ["id2", "01:00", "04:01", "success"],
        ["id3", "02:00", "05:01", "success"],
        ["id4", "03:00", "03:01", "fail"],
        ["id5", "04:00", "07:01", "success"],
        ["id6", "05:00", "08:01", "success"],
        ["id7", "06:00", "09:01", "success"],
        ["id8", "07:00", "10:01", "success"],
        ["id9", "08:00", "11:01", "success"],
        ["id10", "09:00", "12:01", "success"],
        ["id11", "10:00", "13:01", "success"],
        ["id12", "11:00", "14:01", "success"],
        ["id13", "12:00", "15:01", "success"],
        ["id14", "13:00", "16:01", "success"],
        ["id15", "14:00", "17:01", "success"],
        ["id16", "15:00", "18:01", "success"],
        ["id17", "16:00", "19:01", "success"],
        ["id18", "17:00", "20:01", "success"],
        ["id19", "18:00", "21:01", "success"],
        ["id20", "19:00", "22:01", "success"],
        ["id21", "20:00", "23:01", "success"],
        ["id22", "20:05", "23:10", "fail"],

    ]  

def test_with_custom_params():
    # min_delay: 5 minuts
    # max_success: 3
    flights_status_checker = FlightSuccessChecker(flights_data=[
        ["id1", "00:00", "00:05", ""],
        ["id3", "13:00", "13:04", ""], # not enough delay
        ["id2", "02:30", "16:05", ""],
        ["id4", "21:00", "23:00", ""],
        ["id5", "21:01", "23:00", ""], # too many success
        ], min_minutes_delta=5, max_success=3)

    res = flights_status_checker.get_flights_with_success_status()

    assert res == [
        ["id1", "00:00", "00:05", "success"],
        ["id2", "02:30", "16:05", "success"],
        ["id3", "13:00", "13:04", "fail"], # not enough delay
        ["id4", "21:00", "23:00", "success"],
        ["id5", "21:01", "23:00", "fail"], # too many success

    ]
    
