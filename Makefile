.PHONY: great_expectations	

env:
	python -m virtualenv venv && \
	source venv/bin/activate && \
	python -m pip install -r requirements.txt

up:
	docker-compose -f ./local/docker-compose.yml --profile prefect-server up

seed:
	docker-compose -f ./local/docker-compose.yml run dbt-cli "dbt seed"

down:
	docker-compose -f ./local/docker-compose.yml --profile '' --profile prefect-server -v down

ps:
	docker-compose -f ./local/docker-compose.yml ps

prefect-cli:
	docker-compose -f local/docker-compose.yml run prefect-cli

dbt-cli:
	docker-compose -f local/docker-compose.yml run dbt-cli

great_expectations:
	docker-compose -f local/docker-compose.yml run great_expectations	

psql:
	PGPASSWORD=password1234 psql -d dbt -h localhost -p 5433 -U dbt