from flask import Flask, request
import requests 
import uuid
from multiprocessing import Process, Queue, Manager
app = Flask(__name__)


# ROUTER
@app.route('/')
def hello_world():
    return 'Hello'

#recieve request
@app.route('/register', methods= ['GET', 'POST'])
def register():
    global workerIdToUrl
    if verifyRegister(request.form):
        worker = request.form
        idWorker = newWorker(worker, Id())
        # add worker + url to workerIdToUrl hashtable
        workerIdToUrl[idWorker['id']] = idWorker['url'] 
        worker_IdQueue.put(idWorker['id']) 
        
        #print str(workerIdToUrl)
    else:
        return "bad request"

    return 'you made it to router'

#verify Request 
def verifyRegister(req):
    return True if 'port' in req and 'ip' in req else False

#verify Task
def verifyTask(task):
    return True if 'task' in task else False


# add worker to hash Table
def newWorker(form, Id):
    port = form['port']
    ip = form['ip']
    url = 'http://' + ip +':' + port + '/sendwork'
    # url to Newworkerid
    workForce = {'url': url , 'id': Id }
    return workForce

# generate id 
def Id():
    Id = uuid.uuid4()
    return Id

def dispatchLoop():
    import time
    while True:
        #print workerIdToUrl
        time.sleep(.1)
        if not workQueue.empty():
            work_id = workQueue.get()
            for i in xrange(3):
                worker_id = worker_IdQueue.get()
                if work_id in workIdToWorkerList:
                    #if list is empty add initial worker
                    workIdToWorkerList[work_id] = workIdToWorkerList[work_id] + [worker_id, ]
                else:
                    workIdToWorkerList[work_id] = [worker_id, ]
                    # if list is populated add workers
                
                workerIdToWorkId[worker_id] = work_id
                print workerIdToUrl
                print work_id
                r = requests.post(workerIdToUrl[worker_id] , data = workToWorkPath[work_id])




# take in work and delegate work.
@app.route('/work', methods= ['GET', 'POST'])
def assignments():
    if verifyTask(request.form):
        task = request.form 
        workid = uuid.uuid4()
        workToWorkPath[workid] = task
    #task = {'msg':'working Now'}
        workQueue.put(workid)
    #work()
    #print str(task)
    return str(task)

#recieve response
@app.route('/response', methods= ['GET', 'POST'])
def response():
    print request.form
    if request.form == True:
        msg = request.form
    return "got it"

if __name__ == '__main__':

    manager = Manager()
    # work queue
    workQueue = Queue()

    # worker queue
    worker_IdQueue = Queue()

    # status Hash workId w/ status of work
    #status = {'id' : 'state'}

    # workId to workerList id's only infro from /register
    workIdToWorkerList = manager.dict()

    # workerId to workId info from /work
    workerIdToWorkId = manager.dict()

    # workerId to url info from register
    workerIdToUrl = manager.dict()

    # work to workPath info from /work 
    workToWorkPath = manager.dict()
    p = Process(target=dispatchLoop)
    p.start()
    app.run(port= 5000)
