FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Copy shared libraries first
COPY shared_libs/python /app/shared_libs/python
# Install shared libs directly
RUN pip install /app/shared_libs/python

# Copy requirements and remove the local shared_libs line to avoid path issues
COPY services/payment_service/requirements.txt /app/services/payment_service/requirements.txt
RUN sed -i '/shared_libs/d' /app/services/payment_service/requirements.txt
RUN pip install --no-cache-dir -r /app/services/payment_service/requirements.txt

# Copy the rest of the service code
COPY services/payment_service /app/services/payment_service

WORKDIR /app/services/payment_service

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
