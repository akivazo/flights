1. To run the python script that produce the success column:
    If you wish that the result file will be written into a new file:
        $ python ./run_flight_status_checker.py <input_csv> <output_csv>
    If you wish to override the input file:
        $ python ./run_flight_status_checker.py <input_csv>

2. To run the rest api:
    $ python ./run_api.py 


REST Api access example in python:

'''
import requests

new_flights = [
        ["id1", "10:00", "17:00"],
        ["id2", "13:00", "15:00"]
    ]
response = requests.post('http://127.0.0.1:5000/flights', json=new_flights)

response = requests.get('http://127.0.0.1:5000/flights/id1')

print(response.content)
'''

will print:

b'{"arrival":"10:00","departure":"17:00","id":"id1","success":"success"}\n'