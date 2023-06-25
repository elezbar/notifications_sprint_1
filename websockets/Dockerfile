FROM python:3.11-slim

RUN pip install --no-cache-dir --upgrade pip==22.3.1

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

CMD python main.py