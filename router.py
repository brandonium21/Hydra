from flask import Flask, request
import requests 
import uuid
from multiprocessing import Process, Queue, Manager
app = Flask(__name__)


# ROUTER
@app.route('/')
def hello_world():
    return 'Hello'


@app.route('/moreWork', methods= ['GET', 'POST'])
def ready():
    print 'mW active'
    if verifyRegister(request.form):
        port = request.form['port']
        ip = request.remote_addr
        url = 'http://' + ip +':' + port + '/sendwork'
        print 'got url ' + url 
        worker_id = UrlToWorkerId[url]
        print 'got workerId '
        worker_IdQueue.put(worker_id)
        print 'worker: ' + ip +':' + port + " Wants Work"
    return ""

#recieve request
@app.route('/register', methods= ['GET', 'POST'])
def register():
    global workerIdToUrl
    if verifyRegister(request.form):
        port = request.form['port']
        ip = request.remote_addr
        url = 'http://' + ip +':' + port + '/sendwork'
        worker_id = Id()
        UrlToWorkerId[url] = worker_id
        # add worker + url to workerIdToUrl hashtable
        workerIdToUrl[worker_id] = url
        time.sleep(1)
        worker_IdQueue.put(worker_id) 

        # url to Newworkerid
        #print str(workerIdToUrl)
    else:
        return "bad request"

    return 'you made it to router'

#verify Request 
def verifyRegister(req):
    return True if 'port' in req else False

#verify Task
def verifyTask(task):
    return True if 'task' in task else False

def verifyResults(results):
    return True if 'result' in results else False

# generate id 
def Id():
    Id = uuid.uuid4()
    return Id

def dispatchLoop():
    import time
    while True:
        #print workerIdToUrl
        time.sleep(1)
        if not workQueue.empty():
            print 'work in'
            work_id = workQueue.get()
            for i in range(3):
                worker_id = worker_IdQueue.get()
                #print "got worker"
                if work_id in workIdToWorkerList:
                    #if list is empty add initial worker
                    workIdToWorkerList[work_id] = workIdToWorkerList[work_id] + [worker_id, ]
                else:
                    workIdToWorkerList[work_id] = [worker_id, ]
                    # if list is populated add workers
                
                workerIdToWorkId[worker_id] = work_id
                #print workerIdToUrl[worker_id]

                r = requests.post(workerIdToUrl[worker_id] , data = workToWorkPath[work_id])


# take in work and delegate work.
@app.route('/work', methods= ['GET', 'POST'])
def assignments():
    print request.form
    print 'task' in request.form
    print verifyTask(request.form)
    if verifyTask(request.form):
        task = request.form 
        workid = uuid.uuid4()
        workToWorkPath[workid] = task
        print workid
        #task = {'msg':'working Now'}
        workQueue.put(workid, block=False)
        print workQueue
    return str(task)

#recieve response
@app.route('/response', methods= ['GET', 'POST'])
def response():
    #print request.form
    worker = request.form 
    if verifyResults(worker):
        results = worker
        port = worker['port']
        ip = request.remote_addr
        url = 'http://' + ip +':' + port + '/sendwork'
        worker_id = UrlToWorkerId[url]
        work_id = workerIdToWorkId[worker_id]
        resultIdToResults[work_id] = results
        #print str(resultIdToResults[work_id])
    return ""

if __name__ == '__main__':

    manager = Manager()
    # work queue
    workQueue = Queue()

    # worker queue
    worker_IdQueue = Queue()

    # status Hash workId w/ status of work
    #status = {'id' : 'state'}
    UrlToWorkerId = manager.dict()

    resultIdToResults = manager.dict()
    #WorkId to results
    workIdToResults = manager.dict()
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
    app.run(port= 5000, host = 'localhost')
