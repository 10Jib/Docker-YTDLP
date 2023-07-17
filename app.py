import sys
from multiprocessing import pool
from multiprocessing import Queue
import atexit
import logging
from logging.handlers import QueueListener

import flask

from process_functions import callytdl



app = flask.Flask("app")
response_timeout = 1

pool = pool.Pool()  # default is processor count
queue = Queue()

handler = logging.StreamHandler()
process_listner = QueueListener(queue, handler)
app.logger.addHandler(process_listner)
process_listner.start()

def end():  # this dosnt work quite right
    process_listner.stop()
    print("closing pool")
    pool.close()
    print("pool closed")
    process_listner.stop()
    print("stopped listener")

atexit.register(end)  # forcefully closes the pool when needed



def handleProcessResponse(result):  #?
    """Handle response from process and build flask response"""
    if isinstance(result, BaseException):
        return(result, 500)
    else:
        return(result.get('id', 'NO ID FOUND'))


@app.route('/download/<path:url>')
def downloadvideo(url):
    # should check paramaters and throw 400
    # ydl_opts = flask.request.args.get('opts', None)

    result = pool.apply_async(callytdl, args=(url, queue, ))

    result.wait(response_timeout)

    if result.ready():  # if the response is fast, its probably an error
        if isinstance(result, BaseException):
            return(f"Error occured:{result}", 500)
        else:
            app.logger.info(f"Finished Downloading: {result.get().get('id', 'NO ID FOUND')}")
            return(f"Finished Downloading: {result.get().get('id', 'NO ID FOUND')}", 200)

    else:
        return("Download Started...", 200)

    # should have an async waiter to check the result when it comes, but that would be alot
    # tie back, should be a way to check status, or see if a video is downloaded

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)

    process_logger = logging.getLogger(__name__)
    process_logger.debug("proces")

    app.logger.debug("test")
    app.logger.warning("warning")
    logging.debug("debug")