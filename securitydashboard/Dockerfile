ARG BUILD_FROM=ghcr.io/hassio-addons/base-python:3.11
FROM $BUILD_FROM

# Installeer alleen Flask (pip is al aanwezig)
RUN pip3 install --no-cache-dir flask

COPY rootfs/ /

RUN chmod a+x /usr/local/bin/app.py /run.sh

CMD [ "/run.sh" ]
]
