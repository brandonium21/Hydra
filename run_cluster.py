from multiprocessing import Process
import server
import subprocess
import sys
from time import sleep
import signal
import sys
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        run("killall Python")
        sys.exit(0)

def run(cmdline):
    subprocess.Popen(cmdline.split(' '), stdout=sys.stdout)
def run_router():
	run('python ./router.py')
def run_client(port):
	run('python ./client.py ' + str(port))
def run_server(port):
	run('python ./server.py ' + str(port))
if __name__ == '__main__':

	port = 5002
	run_router()
	sleep(1)
	for i in range(int(sys.argv[1])):
		run_server(port + i)
	signal.signal(signal.SIGINT, signal_handler)
	print('Press Ctrl+C')
	signal.pause()
