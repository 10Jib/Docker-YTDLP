FROM python:3.11-alpine3.18 as build

EXPOSE 5500

WORKDIR /APP

COPY . /APP

RUN apk --no-cache add ffmpeg \
    && mkdir /vids \
    && pip install --no-cache-dir -U yt-dlp \
    && pip install --no-cache-dir -U Flask \
    && pip install --no-cache-dir -U gunicorn
    
# start flask 
ENTRYPOINT gunicorn -w 4 app:app -b 0.0.0.0:5500