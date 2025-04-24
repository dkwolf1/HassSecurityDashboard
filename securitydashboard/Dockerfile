ARG BUILD_FROM
FROM $BUILD_FROM

# Om pip goed te laten werken
ENV LANG C.UTF-8

# Vereisten installeren
RUN apk add --no-cache \
    python3 \
    py3-pip \
    bash \
    build-base \
    libffi-dev \
    openssl-dev \
    && pip3 install --upgrade pip setuptools wheel \
    && pip3 install flask

# Bestanden van de rootfs toevoegen
COPY rootfs/ /

# Zorg dat scripts uitvoerbaar zijn
RUN chmod a+x /usr/local/bin/app.py /run.sh

CMD [ "/run.sh" ]
