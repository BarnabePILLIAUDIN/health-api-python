include .env
export
.PHONY: init run test build clean

init: SHELL:=/bin/bash  
init:
	@echo "WARNING: If you have not created .env file interrupt the script, create and fill the file, relaunch the script"
	@echo "Initializing the project by creating the container and running them"
	@make build
	@make run
	@make test

run:
	@echo running api container
	@docker run -p 3000:3000 --name python-api-bp -d api-python-msi-do-1b-bp:latest

test:
	@echo "Running tests to ensure the api is well installed and running"
	@docker exec python-api-bp python3 /app/src/test.py

build:
	@echo "Building image of the api"
	@docker build -t api-python-msi-do-1b-bp:latest .