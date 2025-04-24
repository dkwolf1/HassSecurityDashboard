ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Installeer Python, pip en bash correct
RUN apk add --no-cache python3 py3-pip bash \
    && python3 -m ensurepip \
    && pip3 install --no-cache-dir --upgrade pip \
    && pip3 install flask

COPY rootfs/ /

RUN chmod a+x /usr/local/bin/app.py /run.sh

CMD [ "/run.sh" ]
