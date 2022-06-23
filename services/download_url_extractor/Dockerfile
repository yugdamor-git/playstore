FROM mcr.microsoft.com/playwright/python:v1.21.0-focal

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

RUN playwright install

RUN playwright install-deps

COPY . .

CMD [ "python","downloader.py" ]