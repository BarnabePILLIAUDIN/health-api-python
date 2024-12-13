# Health API

## Description

This api will allow you to know your BMI and your BMR.

- To know your BMI you need to send your `weight` and `height` in the body of the request on the `/bmi` endpoint. The weight should be in `kg` and the height should be in `m`.
- To know your BMR you need to send your `weight`, `height`, `age`, and `gender` in the body of the api on the `/bmr` endpoint. The weight should be in `kg`, the height should be in `cm`, the age should be in `year` and gender should be either `male or female`.

## Installation

- To install the project
- Clone the project
- Run cp .env.example .env
- Fill the .env file with the right values

### To launch it with docker (recommanded)

- run `make init-container` it will build the image of the api, start the container and run the test to make sure everything is working fine.

**_If you are on windows you can run the following commands and you don't have make (on MacOs and Linux make should be installed by default) you can run the following commands:_**

- `docker build -t api-python-msi-do-1b-bp:latest .`
- `docker run -p 3000:3000 --name python-api-bp -d api-python-msi-do-1b-bp:latest`
- `docker exec -it python-api-bp python src/test.py`

### To run it with a virtual environment

- Run `make-init`
- To test the api run `make test-api`

**_If you are on windows you can run the following commands and you don't have make (on MacOs and Linux make should be installed by default) you can run the following commands:_**

- Create a virtual environment `python3 -m venv venv`
- Activate the virtual environment `source venv/bin/activate`
- Install the dependencies `pip install -r requirements.txt`
- Start the app `python src/app.py`
- Run the tests `python src/test.py`

# Warning

- The tests are composed of unit tests and api tests. So you need the api to be running to run the tests.
