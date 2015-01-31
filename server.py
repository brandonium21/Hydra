
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
resRouter = 'http://192.168.1.122:5000/response'
router = 'http://192.168.1.122:5000/register'
moreWork = 'http://192.168.1.122:5000/moreWork'

@app.route('/sendwork', methods= ['GET', 'POST'])
def sendwork():
       
        if routerMsg(request.form):
            task = request.form
            q.put(task)

        else:
            return "No Task"

        return "got it"

def workLoop():
    import time
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
            print r.text

#return results of work to the roter
def results(result):
    results = {'result': result}
    r = requests.post(resRouter, data= results)

#verify msg sent Back
def routerMsg(task):
    return True if 'task' in task else False

def done():
    r = requests.post(moreWork, data= port)
# SERVER
def state():
    r = requests.post(router, data= port)



if __name__ == '__main__':
    p = Process(target=workLoop)
    p.start()
    
    port = {'port':sys.argv[1]}
    state();
    app.run(host = '198.168.1.101' ,port= int(sys.argv[1]))
