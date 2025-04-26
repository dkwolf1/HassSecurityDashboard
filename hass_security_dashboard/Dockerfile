ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.18
FROM ${BUILD_FROM}

ENV LANG C.UTF-8

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache python3 py3-pip py3-numpy py3-gcc py3-setuptools nmap

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

CMD [ "bash", "/app/run.sh" ]
