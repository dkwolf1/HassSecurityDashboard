FROM python:3.11-slim
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean
WORKDIR /app
COPY app/ /app/
COPY run.sh /run.sh
COPY web/ /app/web/
RUN chmod +x /run.sh
RUN pip install flask waitress
EXPOSE 5000
CMD ["/run.sh"]