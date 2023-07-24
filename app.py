import logging
import re

import flask

from process_functions import startytdl, init


app = flask.Flask("app")
#init(logging.Logger)

def validateRequest(url, params=None):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # should check for valid parameters 

    # should check for any non fstrings?
    assert re.match(regex, url) is not None


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

    # should validate it wont download videos for no reason?
    app.logger.debug(f"Reveived Request, starting ytdl: {url}")
    result = startytdl(url, )
    return(result)

    # should have an async waiter to check the result when it comes, but that would be alot
    # tie back, should be a way to check status, or see if a video is downloaded

if __name__ == '__main__':
    
    logging.getLogger().setLevel(logging.DEBUG)
    app.logger.debug("starting multi processing")
    init(app.logger)

    app.run()