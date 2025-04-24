FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && \
    apt-get install -y bash curl && \
    pip install flask
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["/bin/bash", "/app/run.sh"]
