FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY shared_libs/python /app/shared_libs/python
RUN pip install /app/shared_libs/python
COPY services/order_service/requirements.txt /app/services/order_service/requirements.txt
RUN sed -i '/shared_libs/d' /app/services/order_service/requirements.txt
RUN pip install --no-cache-dir -r /app/services/order_service/requirements.txt

COPY services/order_service /app/services/order_service

WORKDIR /app/services/order_service

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
