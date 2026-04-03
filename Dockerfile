FROM python:3.14-alpine

RUN apk add qt5-qtdeclarative-dev

COPY run-qmlformat.py /run-qmlformat.py

ENTRYPOINT ["/run-qmlformat.py"]
