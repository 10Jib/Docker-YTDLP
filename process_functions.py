from multiprocessing import pool
from multiprocessing import current_process
from multiprocessing import Process
from logging.handlers import QueueHandler
import logging
from os import getpid

import yt_dlp
from yt_dlp.utils import YoutubeDLError

#formatter = logging.Formatter('%(threadName)s: %(message)s')


default_ydl_opts = {'format':"mp4"}

def callytdl(url, loggerQueue, params=default_ydl_opts):
    logger = logging.getLogger(__name__)  # maybe a better name
    logger.addHandler(QueueHandler(loggerQueue))

    params["logger"] = logger

    logger.debug(f"callytdl from pid:{getpid()} with params:{params.items()}")

    try:
        with yt_dlp.YoutubeDL(params) as ydl:
            result = ydl.extract_info(url)
            # show the post with the given id, the id is an integer

    except YoutubeDLError as e:
        logger.error(f"YTDLP Error: {e}")
        return e
    except Exception as e:
        logger.error(f"Failed to download video from process: {e}")
        return e
    else:
        return result
