FROM python:3.11-slim

WORKDIR /app

COPY app /app
COPY web /app/web
COPY run.sh /run.sh

RUN pip install flask && chmod +x /run.sh

EXPOSE 5000

CMD ["/run.sh"]