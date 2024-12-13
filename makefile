# By default sh is used by default but source command is not available in sh
SHELL:=/bin/bash  
include .env
export
.PHONY: init run test build clean

init:
	@make setup-env
	@make run


setup-env:
	@echo "Ensuring that venv is creating"
	@python3 -m venv venv
	@echo "Ensuring that the venv is activated"
	@source venv/bin/activate
	@echo "Ensuring that the requirements are satisfied"
	@pip install -r requirements.txt

# I know I used python3 to create venv but using just python ensure that the venv is used because this alias doesn't exist outside of venv in mac and linux 
run:
	@echo "Running the app in the venv"
	@make setup-env
	@python src/app.py

test-api:
	@echo "Testing the api via the virtual environment"
	@make setup-env
	@python src/test.py

init-container:
	@echo "WARNING: If you have not created .env file interrupt the script, create and fill the file, relaunch the script"
	@echo "Initializing the project by creating the container and running them"
	@make build
	@make run-container
	@make test-container

run-container:
	@echo running api container
	@docker run -p ${MAKE_HOST_PORT}:${API_PORT} --name ${MAKE_CONTAINER_NAME} -d ${MAKE_IMAGE_NAME}

test-container:
	@echo "Running tests to ensure the api is well installed and running"
	@docker exec ${MAKE_CONTAINER_NAME} python3 /app/src/test.py

build:
	@echo "Building image of the api"
	@docker build -t ${MAKE_IMAGE_NAME} .

stop-container:
	@echo "Stopping the containers"
	@docker stop ${MAKE_CONTAINER_NAME}