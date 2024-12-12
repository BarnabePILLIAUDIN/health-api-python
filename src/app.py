from os import getenv, path

from dotenv import load_dotenv
from flask import Flask, request

from utils.health_utils import calculate_bmi, calculate_bmr
from utils.request_utils import InvalidRequest, sanitize_body, send_response

load_dotenv(dotenv_path=path.join(path.dirname(__file__), "../.env"))

PORT=getenv("API_PORT")
HOST=getenv("API_HOST")

if not PORT or not HOST:
    raise Exception("API_PORT and API_HOST are required in .env file")

app = Flask(__name__)

@app.route("/bmi", methods=['POST'])
def bmi():

  try: 
    body = sanitize_body(request, ["height", "weight"])
  except InvalidRequest as e:
    return send_response(status=400, message=e.message)
  
  bmi = calculate_bmi(body["height"], body["weight"])
  if not bmi:
    return send_response(status=400, message="Invalid request check your inputs. Height and weight must be greater than 0")
  
  return send_response(data={"bmi":calculate_bmi(body["height"], body["weight"])})

@app.route("/bmr", methods=['POST'])
def bmr():
    try: 
      body = sanitize_body(request, ["height", "weight", "age", "gender"])
    except InvalidRequest as e:
        return send_response(status=400, message=e.message)
    
    bmr = calculate_bmr(body["height"], body["weight"], body["age"], body["gender"])
    if bmr is None:
        return send_response(status=400, message="Invalid request check your inputs. The correct genders are male or female, height, weight and age must be greater than 0")
    return send_response(data={"bmr":bmr})


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
