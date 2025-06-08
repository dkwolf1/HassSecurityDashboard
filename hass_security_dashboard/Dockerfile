ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.18
FROM ${BUILD_FROM}

ENV LANG C.UTF-8

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache \
        python3 \
        py3-pip \
        python3-dev \
        musl-dev \
        gcc && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]

