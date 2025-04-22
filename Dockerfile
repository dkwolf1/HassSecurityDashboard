FROM python:3.11-slim

WORKDIR /app
COPY app/ /app/
COPY run.sh /run.sh
RUN chmod +x /run.sh
RUN pip install flask requests netifaces cryptography paho-mqtt pyyaml

COPY web/ /app/web/
EXPOSE 5000
CMD [ "/run.sh" ]
