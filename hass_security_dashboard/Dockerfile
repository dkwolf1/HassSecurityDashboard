FROM python:3.11-slim
RUN apt-get update && apt-get install -y python3-pip net-tools iputils-ping && apt-get clean
WORKDIR /app
COPY app/ /app/
COPY web/ /app/web/
COPY run.sh /run.sh
RUN chmod +x /run.sh
RUN pip install flask waitress
EXPOSE 5000
CMD ["/run.sh"]