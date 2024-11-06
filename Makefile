.PHONY: build up ssh server down flake8 test

build:
	docker compose up --build -d

up:
	docker compose up -d

ssh:
	docker exec -it linkgraph-toy-blogapp /bin/bash

migrate:
	docker exec linkgraph-toy-blogapp python manage.py migrate

server:
	docker exec linkgraph-toy-blogapp python manage.py runserver 0.0.0.0:5700

down:
	docker compose down

flake8:
	docker exec linkgraph-toy-blogapp flake8 .

test:
	docker exec linkgraph-toy-blogapp python manage.py test
