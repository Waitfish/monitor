FROM python:3.6-alpine
EXPOSE 5000
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV ES_URL http://127.0.0.1:9200

CMD [ "python", "./index.py" ]
