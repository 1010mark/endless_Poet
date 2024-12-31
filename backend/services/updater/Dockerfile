FROM python:3.11

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /updater

COPY ./services/updater /updater
COPY ./tools /updater/tools
COPY ./resources /updater/resources

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]