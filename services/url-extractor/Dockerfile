FROM mcr.microsoft.com/playwright/python:v1.22.0-focal

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD [ "python","-u","url_extractor.py" ]