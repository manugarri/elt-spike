env:
	python -m virtualenv venv && \
	source venv/bin/activate && \
	python -m pip install -r requirements.txt


# cd . is a hack to fix a weird WSL2 docker issue
up:
	cd . && docker-compose -f ./local/docker-compose.yml up

down:
	cd . && docker-compose -f ./local/docker-compose.yml down

ps:
	cd . && docker-compose -f ./local/docker-compose.yml ps

prefect-cli:
	cd . && docker-compose -f local/docker-compose.yml run prefect-cli

dbt-cli:
	cd . && docker-compose -f local/docker-compose.yml run dbt-cli
