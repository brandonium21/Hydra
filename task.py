import requests
task = {'task': 'ls'}
r = requests.post('http://127.0.0.1:5000/work', data = task)