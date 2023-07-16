from multiprocessing import pool
import logging
from os import getpid

import yt_dlp


process_logger = logging.getLogger(__name__)
default_ydl_opts = {'format':"mp4", "logger":process_logger}

def callytdl(url, logger=process_logger, params=default_ydl_opts):
    logger.debug(f"callytdl from pid:{getpid()} with params:{params.items()}")

    try:
        with yt_dlp.YoutubeDL(params) as ydl:
            result = ydl.extract_info(url)
            # show the post with the given id, the id is an integer
    except Exception as e:
        logger.error(f"Failed to download video from process: {e}")
        return e
    
    return result