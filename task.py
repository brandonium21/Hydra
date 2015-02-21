import requests
task = {'task': 'docker run ubuntu:14.04 /bin/sh -c "sleep 1; echo helloworld"'}
r = requests.post('http://127.0.0.1:5000/work', data = task)