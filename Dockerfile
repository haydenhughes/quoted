FROM python:3.8.3-alpine3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 5000
CMD python -m quoted
