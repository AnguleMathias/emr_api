# Define filename references
DEV_FOLDER := docker/
DEV_COMPOSE_FILE := docker/docker-compose.yml

# Set target lists
.PHONE: help

help:
	@echo ''
	@echo 'Usage:'
	@echo '${YELLOW} make ${RESET} ${GREEN}<target> [options]${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		message = match(lastLine, /^## (.*)/); \
		if (message) { \
			command = substr($$1, 0, index($$1, ":")-1); \
			message = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} %s\n", command, message; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo ''

build:
	@ echo "Building emr..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} up -d
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app ${DEV_FOLDER}/start_app.sh

status:
	@ echo "Checking status..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} ps

create:
	@ echo 'Creating $(service) service...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} create $(service)

start:
	@ echo 'Starting  $(service) service...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} start $(service)

run-app:
	@ echo 'Running emr_api on port 8000...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app ${DEV_FOLDER}/start_app.sh

stop:
	@ echo 'Stopping $(service) service...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} stop $(service)

restart:
	@ echo 'restarting $(service) service...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} stop $(service)
	@ docker-compose -f ${DEV_COMPOSE_FILE} rm -f -v $(service)
	@ docker-compose -f ${DEV_COMPOSE_FILE} create --force-recreate $(service)
	@ docker-compose -f ${DEV_COMPOSE_FILE} start $(service)

migrate-initial:
	@ echo 'Running initial migrations...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app ${DEV_FOLDER}/start_initial_migrations.sh "$(message)"

migrate:
	@ echo 'Running migrations...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app ${DEV_FOLDER}/start_migrations.sh "$(message)"

import:
	@ echo "importing database..."
	@ docker cp ${DEV_FOLDER}/start_db_import.sh emr_user:/
	@ docker cp $(dump) emr_user:/
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec database /start_db_import.sh $(dump)

ssh:
	@ echo 'ssh...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec $(service) /bin/bash

down:
	@ echo "emr going down..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} down

services:
	@ echo "Getting services..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} ps --services

remove:
	@ echo "Removing $(service) container"
	@ docker-compose -f ${DEV_COMPOSE_FILE} rm -f -v $(service)

clean: down
	@ echo "Removing containers..."
	@ docker stop emr_user emr_api
	@ docker rm emr_user emr_api

kill:
	@ echo "killing..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} kill -s SIGINT