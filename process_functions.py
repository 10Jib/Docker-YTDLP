from multiprocessing.pool import Pool
from multiprocessing import get_context
from multiprocessing import Queue
from logging.handlers import QueueHandler
from logging.handlers import QueueListener

import atexit
import logging
from os import getpid

import yt_dlp
from yt_dlp.utils import YoutubeDLError

default_ydl_opts = {'format':"mp4"}
response_timeout = 1

# params too
"""cant be in the same module, but cant not be in the same moduel"""
def startytdl(url, callback=None, params=None):
    """For starting the ytdl process, and handling the variety of its outcomes."""
    if params:
        result = pool.apply_async(callytdl, args=(url, params, ))
    else:
        result = pool.apply_async(callytdl, args=(url, ))
        
    #return(result)
    result.wait(response_timeout)

    if result.ready():  # if the response is fast, its probably an error
        if isinstance(result, BaseException):
            return(f"Error occured:{result}", 500)
        else:
            #logging.info(f"Finished Downloading: {result.get().get('id', 'NO ID FOUND')}")
            return(f"Finished Downloading: {result.get().get('id', 'NO ID FOUND')}", 200)

    else:
        return("Download Started...", 200)

def callytdl(url, params=default_ydl_opts):
    # shouldnt need this  global queue
    logger = logging.getLogger(__name__)  # maybe a better name
    logger.addHandler(QueueHandler(queue))

    params["logger"] = logger

    logger.debug(f"callytdl from pid:{getpid()} with params:{params.items()}")

    try:
        with yt_dlp.YoutubeDL(params) as ydl:
            result = ydl.extract_info(url)
            # show the post with the given id, the id is an integer

    except YoutubeDLError as e:
        logger.error(f"YTDLP Error: {e}")
        return e
    
    # should this be caught here??
    except Exception as e:
        logger.error(f"Failed to download video from process: {e}")
        return e
    else:
        return result

def init(logger):

    logging.info("starting queue resources")

    ctx = get_context('fork')

    global queue
    queue = ctx.Queue()

    global pool
    pool = ctx.Pool()  # default is processor count

    handler = logging.StreamHandler()
    process_listner = QueueListener(queue, handler)
    logger.addHandler(process_listner)
    process_listner.start()
    logging.info("setup finished")
    #formatter = logging.Formatter('%(threadName)s: %(message)s')

    def end():  # this dosnt work quite right
        process_listner.stop()
        print("closing pool")
        pool.close()
        print("pool closed")
        pool.join()
        print("stopped listener")

    atexit.register(end)  # forcefully closes the pool when needed


# so this would need to be a class
# because I need something external to initiate the global vars
# then those vars are inherited