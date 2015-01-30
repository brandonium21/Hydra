
from flask import Flask
from flask import redirect, render_template
from flask import request, url_for
import sys
import os
from multiprocessing import Process, Queue
app = Flask(__name__)
import requests

q = Queue()
resRouter = 'http://127.0.0.1:5000/response'

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
            os.system(
                item['task']
                )
            r = requests.post(resRouter, data = item)
            print r.text


#verify msg sent Back
def routerMsg(task):
    return True if 'task' in task else False

# SERVER
def state():
    router = 'http://127.0.0.1:5000/register'
    r = requests.post(router, data= port)



if __name__ == '__main__':
    p = Process(target=workLoop)
    p.start()
    
    port = {'port':sys.argv[1],
            'ip':'127.0.0.1'}
    state();
    app.run(port= int(sys.argv[1]))
