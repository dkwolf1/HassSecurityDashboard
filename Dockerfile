ARG BUILD_FROM
FROM ${BUILD_FROM} AS base
LABEL maintainer="Dennis Verpleegkundige <you@example.com>"

# Install runtime dependencies
RUN apk add --no-cache \
    nginx \
    s6-overlay \
    openssl \
    nmap \
    curl

# Copy add-on files
COPY rootfs/ /

# Expose if ingress disabled
EXPOSE 8123

ENTRYPOINT ["/init"]