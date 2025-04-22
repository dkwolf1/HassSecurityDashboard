FROM python:3.11-slim

# Install system dependencies required by pip packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libffi-dev \
        libssl-dev \
        python3-dev \
        iputils-ping \
        net-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy application and web assets
COPY app/ /app/
COPY run.sh /run.sh
COPY web/ /app/web/

# Set permissions
RUN chmod +x /run.sh

# Install required Python packages
RUN pip install --no-cache-dir \
    flask \
    requests \
    netifaces \
    cryptography \
    paho-mqtt \
    pyyaml \
    waitress

# Expose Flask port for Ingress
EXPOSE 5000

# Launch script
CMD ["/run.sh"]
