run:
	docker-compose build
	docker-compose up -d
stop:
	docker-compose down
enter:
	docker-compose exec horse-info-crawler /bin/bash
start:
	docker-compose exec horse-info-crawler pipenv run start
test:
	docker-compose exec horse-info-crawler pipenv run test
lint:
	docker-compose exec horse-info-crawler pipenv run lint
format:
	docker-compose exec horse-info-crawler pipenv run format
log:
	docker-compose logs -f horse-info-crawler