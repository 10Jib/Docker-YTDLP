from multiprocessing.pool import Pool
from multiprocessing import get_context
from multiprocessing import Queue
from logging.handlers import QueueHandler
from logging.handlers import QueueListener

import atexit
import logging
from os import getpid

print("code is running")
test = "test"

def end():  # this dosnt work quite right
    process_listner.stop()
    print("closing pool")
    pool.close()
    print("pool closed")
    pool.join()
    process_listner.stop()
    print("stopped listener")

atexit.register(end)  # forcefully closes the pool when needed

response_timeout = 1

ctx = get_context('fork')

global pool
pool = ctx.Pool()  # default is processor count

global queue
queue = ctx.Queue()

handler = logging.StreamHandler()
process_listner = QueueListener(queue, handler)
#app.logger.addHandler(process_listner)
process_listner.start()
#formatter = logging.Formatter('%(threadName)s: %(message)s')