FROM python:3.14-slim-bookworm

COPY nexus_upload.py /opt/nexus_upload.py

RUN pip install requests
