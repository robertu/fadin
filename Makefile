
all: build

.env:
	cp .env-sample .env

up:
	docker-compose up

build: .env
	docker-compose build

test:
	docker-compose run web pytest

shell:
	docker-compose exec web bash
