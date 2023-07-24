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


default_ydl_opts = {'format':"mp4", "quiet":True, "noplaylist":True}
response_timeout = 1

def startytdl(url, params=None, callback=None):
    """For starting the ytdl process, and handling the variety of its outcomes."""
    if params:
        result = pool.apply_async(callytdl, args=(url, params, ))
    else:
        result = pool.apply_async(callytdl, args=(url, ))
        
    result.wait(response_timeout)

    if result.ready():  # if the response is fast, its probably an error
        try:
            id = result.get().get('id', 'NO ID FOUND')
        except AttributeError as e:
            logging.exception(f"Failed to get result. Probably because incorect usage: {e}")
            return("Incorrect Usage of YTDLP", 500)
        else:
            return(f"Finished Downloading: {id}", 200)

    else:
        return("Download Started...", 200)

def callytdl(url, params=default_ydl_opts):
    # shouldnt need this  global queue
    logger = logging.getLogger("callytdlp")  # maybe a better name
    logger.addHandler(QueueHandler(queue))
    logger.setLevel(logging.DEBUG)

    params["logger"] = logger  # this might be hard with multiproc

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

def init(logger=None):
    global init
    init = True

    if logger:
        logger.info("starting queue resources")

    ctx = get_context('fork')

    global queue
    queue = ctx.Queue()

    global pool
    pool = ctx.Pool()  # default is processor count

    if logger:
        process_listner = QueueListener(queue, *logger.handlers)  # something isnt right here...
        process_listner.start()
        logging.info("setup finished")

    def end():  # this dosnt work quite right
        process_listner.stop()
        print("closing pool")
        pool.close()
        print("pool closed")


    atexit.register(end)  # forcefully closes the pool when needed


# so this would need to be a class
# because I need something external to initiate the global vars
# then those vars are inherited