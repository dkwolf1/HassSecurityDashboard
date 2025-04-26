ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.18
FROM ${BUILD_FROM}

ENV LANG C.UTF-8

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-numpy gcc nmap && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "/app/run.sh"]

