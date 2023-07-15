import sys

import flask
import yt_dlp

app = flask.Flask("app")

@app.route('/download/<path:url>')
def downloadvideo(url):
    # should check paramaters and throw 400
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            # show the post with the given id, the id is an integer
    except Exception as e:
        return f"Error occured:{e}", 500  # not secure to send raw error messages
    return "OK", 200

# def configure():
#     pass

# if __name__ == '__main__':
#     configure()
#     being_debugged = sys.gettrace() is not None
#     app.run(debug=being_debugged)
# else:
#     configure()