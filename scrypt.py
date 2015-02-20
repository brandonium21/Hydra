import os
import subprocess
import requests
import sys

task = {'task': 'ls'}
router = {'router': 'python router.py'}
# start ROUTER
def runRouter():
	result = subprocess.check_output([
	    item['router']], 
	    shell=True
	)
	print result
	return result
# start SERVERS


# run TASK
