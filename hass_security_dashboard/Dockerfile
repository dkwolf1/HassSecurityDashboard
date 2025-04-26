FROM debian:bullseye-slim

WORKDIR /app

COPY requirements.txt /app/
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev nmap gcc && \
    pip3 install --no-cache-dir -r /app/requirements.txt

COPY . /app/

CMD ["bash", "/app/run.sh"]
