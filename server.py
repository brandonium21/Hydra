import sys
from logging import warning, info , error, debug, critical, DEBUG, basicConfig
import time
basicConfig(stream=sys.stdout, level=DEBUG,  format = "[%(filename)s:%(lineno)s - %(funcName)1s() ] %(message)s")
from flask import Flask
from flask import redirect, render_template
from flask import request, url_for
import sys
import os
import subprocess
from multiprocessing import Process, Queue
app = Flask(__name__)
import requests

q = Queue()
host = 'localhost'
resRouter = 'http://' + host + ':5000/response'
router = 'http://' + host + ':5000/register'
moreWork = 'http://' + host + ':5000/moreWork'
port = 0
blah = {'port':sys.argv[1]}
@app.route('/sendwork', methods= ['GET', 'POST'])
def sendwork():
        if routerMsg(request.form):
            task = request.form
            q.put(task)

        else:
            return "No Task"

        return "got it"

def workLoop():

    while True:
        time.sleep(.1)
        if not q.empty():
            item = q.get()
            #print str(item)
            result = subprocess.check_output([
                item['task']], 
                shell=True
                )
            results(result)
            r = requests.post(resRouter, data = item)
            done();
            print r.text

#return results of work to the roter
def results(result):
    results = {'result': result}
    r = requests.post(resRouter, data= results)

#verify msg sent Back
def routerMsg(task):
    return True if 'task' in task else False

def done():
    info(blah)
    m = requests.post(moreWork, data= blah)
# SERVER
def state():
    r = requests.post(router, data= blah)



if __name__ == '__main__':
    p = Process(target=workLoop)
    p.start()
    
    blah = {'port':sys.argv[1]}
    state();
    app.run(host = host , port= int(sys.argv[1]))
