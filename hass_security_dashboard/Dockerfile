ARG BUILD_FROM
FROM ${BUILD_FROM} AS base
LABEL maintainer="dkwolf1"

# 1) Installeer systeem-deps
RUN apk add --no-cache \
    s6-overlay \
    openssl \
    nmap \
    curl \
    # voor eventuele nginx-proxy (optioneel)
    nginx

# 2) Copy backend code en installeer Python-deps
COPY hass_security_dashboard/app/dashboard /app/dashboard
WORKDIR /app/dashboard
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copy rootfs (entrypoints, www, services)
COPY hass_security_dashboard/rootfs/ /

# 4) Poort als ingress uitstaat
EXPOSE 8123

ENTRYPOINT ["/init"]
