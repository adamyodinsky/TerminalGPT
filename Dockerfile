FROM python:3.13-alpine

RUN pip install terminalgpt

ENTRYPOINT ["terminalgpt"]
