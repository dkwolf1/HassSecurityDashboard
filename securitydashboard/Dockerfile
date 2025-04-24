ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

RUN apk add --no-cache python3 py3-pip bash \
    && pip install flask

COPY rootfs/ /

RUN chmod a+x /usr/local/bin/app.py /run.sh

CMD [ "/run.sh" ]
