FROM mcr.microsoft.com/playwright/python:v1.21.0-focal

RUN apt-get update && DEBIAN_FRONTEND="noninteractive" TZ="Europe/Moscow" apt-get install -y tzdata

# === INSTALL Python ===
RUN apt-get update && apt-get install -y python3.9 python3-pip && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git gnupg2

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils


WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

RUN playwright install

RUN playwright install-deps

COPY . .

CMD [ "xvfb-run","python","downloader.py" ]