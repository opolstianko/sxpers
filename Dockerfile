FROM python:3.6-alpine3.6

RUN apk add --no-cache --virtual build-dependencies libffi-dev make gcc python3-dev linux-headers musl-dev openssl-dev && \
    pip3 install cffi sanic aiogcd aiohttp aioredis asyncio_extras && \
    apk del build-dependencies

RUN apk add --no-cache openssl

ADD . /app/app.py

WORKDIR /app

EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]