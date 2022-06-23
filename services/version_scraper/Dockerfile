FROM mcr.microsoft.com/playwright/python:v1.21.0-focal

WORKDIR /usr/src/app

COPY ./requirements.txt ./

# RUN apt-get -y update && apt-get -y install python3 && apt-get -y install python3-pip

RUN pip install -r requirements.txt

RUN playwright install

RUN playwright install-deps

COPY . .

CMD [ "python","version_scraper.py" ]