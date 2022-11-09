env:
	python -m virtualenv venv && \
	source venv/bin/activate && \
	python -m pip install -r requirements.txt

up:
	docker-compose -f ./local/docker-compose.yml up

seed:
	docker-compose -f ./local/docker-compose.yml run dbt-cli "dbt seed"

down:
	docker-compose -f ./local/docker-compose.yml down

ps:
	docker-compose -f ./local/docker-compose.yml ps

prefect-cli:
	docker-compose -f local/docker-compose.yml run prefect-cli

dbt-cli:
	docker-compose -f local/docker-compose.yml run dbt-cli

