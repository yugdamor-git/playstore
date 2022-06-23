FROM mcr.microsoft.com/playwright/python:v1.21.0-focal

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

RUN playwright install

RUN playwright install-deps

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w 3", "-b", "0.0.0.0:5000", "main:app"]