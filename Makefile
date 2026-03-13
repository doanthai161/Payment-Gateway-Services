.PHONY: lint format test build-all help

help:
	@echo "Available commands:"
	@echo "  make lint       : Run flake8, black, and isort checks"
	@echo "  make format     : Run black and isort to format code"
	@echo "  make test       : Run all tests"
	@echo "  make build-all  : Build all docker images"

lint:
	flake8 .
	black . --check
	isort . --check-only

format:
	isort .
	black .

test:
	pytest shared_libs/python
	cd services/order_service && python manage.py test
	cd services/payment_service && python manage.py test
	cd services/notification_service && python manage.py test

build-all:
	docker build -t order-service -f services/order_service/Dockerfile .
	docker build -t payment-service -f services/payment_service/Dockerfile .
	docker build -t notification-service -f services/notification_service/Dockerfile .
