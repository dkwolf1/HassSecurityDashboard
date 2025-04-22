FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential gcc libffi-dev libssl-dev python3-dev iputils-ping net-tools && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/ /app/
COPY run.sh /run.sh
RUN chmod +x /run.sh
COPY web/ /app/web/
RUN pip install --no-cache-dir flask requests netifaces cryptography paho-mqtt pyyaml waitress

EXPOSE 5000
CMD ["/run.sh"]