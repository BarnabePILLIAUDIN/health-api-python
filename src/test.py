import unittest
from os import getenv, path

import requests
from dotenv import load_dotenv

from utils.health_utils import calculate_bmi, calculate_bmr

load_dotenv(dotenv_path=path.join(path.dirname(__file__), "../.env"))

PORT =  getenv("TEST_API_PORT")
API_HOST = getenv("TEST_API_HOST")

if not PORT or not API_HOST or len(PORT) == 0 or len(API_HOST) == 0:
    raise Exception("TEST_API_PORT and TEST_API_HOST are required in .env file")

API_URL = f"http://{API_HOST}:{PORT}"
HEADERS = {"Content-Type": "application/json"}

def base_request(endpoint, data):
    return requests.post(f"{API_URL}/{endpoint}", json=data, headers=HEADERS)

class TestFunction(unittest.TestCase):

# Test for BMI

# Normal use case
    def test_normal_use_bmi(self):
        """Test BMI calculation with normal values."""
        self.assertAlmostEqual(calculate_bmi(1.75, 70), 22.86,places=2)
        self.assertAlmostEqual(calculate_bmi(2, 100), 25.00,places=2)
        self.assertAlmostEqual(calculate_bmi(0.70, 10), 20.41,places=2)

# Missing values
    def test_missing_height_bmi(self):
        """Test BMI calculation with missing height."""
        self.assertIsNone(calculate_bmi(None, 70))
    
    def test_missing_weight_bmi(self):
        """Test BMI calculation with missing weight."""
        self.assertIsNone(calculate_bmi(1.75, None))

# Incorrect values (zero, negative)
    def test_negative_weight_bmi(self):
        """Test BMI calculation with negative weight."""
        self.assertIsNone(calculate_bmi(1.75, -70))
    
    def test_negative_height_bmi(self):
        """Test BMI calculation with negative height."""
        self.assertIsNone(calculate_bmi(-1.75, 70))

    def test_zero_height_bmi(self):
        """Test BMI calculation with zero height."""
        self.assertIsNone(calculate_bmi(0, 70))

    def test_zero_weight_bmi(self):
        """Test BMI calculation with zero weight."""
        self.assertIsNone(calculate_bmi(1.75, 0))
    
    def test_empty_height_bmi(self):
        """Test BMI calculation with empty height."""
        self.assertIsNone(calculate_bmi("", 70))
    
    def test_empty_weight_bmi(self):
        """Test BMI calculation with empty weight."""
        self.assertIsNone(calculate_bmi(1.75, ""))

# Test for BMR

# Normal use case
    def test_normal_use_bmr_male(self):
        """Test BMR calculation with normal values."""
        self.assertAlmostEqual(calculate_bmr(175, 70, 25, "male"), 1724.05, places=2)
    
    def test_normal_use_bmr_female(self):
        """Test BMR calculation with normal values."""
        self.assertAlmostEqual(calculate_bmr(165, 60,25, "female"), 1405.33 , places=2)

# Missing values
    def test_missing_height_bmr(self):
        """Test BMR calculation with missing height."""
        self.assertIsNone(calculate_bmr(None, 70, 25, "male"))

    def test_missing_weight_bmr(self):
        """Test BMR calculation with missing weight."""
        self.assertIsNone(calculate_bmr(175, None, 25, "male"))

    def test_missing_age_bmr(self):
        """Test BMR calculation with missing age."""
        self.assertIsNone(calculate_bmr(175, 70, None, "male"))
    
    def test_missing_gender_bmr(self):
        """Test BMR calculation with missing gender."""
        self.assertIsNone(calculate_bmr(175, 70, 25, None))
    
# Incorrect values (negative, zero, incorrect gender)
    def test_negative_height_bmr(self):
        """Test BMR calculation with negative height."""
        self.assertIsNone(calculate_bmr(-175, 70, 25, None))

    def test_negative_weight_bmr(self):
        """Test BMR calculation with negative weight."""
        self.assertIsNone(calculate_bmr(175, -70, 25, None))
    
    def test_negative_age_bmr(self):
        """Test BMR calculation with negative age."""
        self.assertIsNone(calculate_bmr(175, 70, -25, None))

    def test_incorrect_gender_bmr(self):
        """Test BMR calculation with incorrect gender."""
        self.assertIsNone(calculate_bmr(175, 70, 25, "emale"))

    def test_zero_height_bmr(self):
        """Test BMR calculation with zero height."""
        self.assertIsNone(calculate_bmr(0, 70, 25, None))

    def test_zero_weight_bmr(self):
        """Test BMR calculation with zero weight."""
        self.assertIsNone(calculate_bmr(175, 0, 25, None))
    
    def test_zero_age_bmr(self):
        """Test BMR calculation with zero age."""
        self.assertIsNone(calculate_bmr(175, 70, 0, None))
    
    def test_empty_height_bmr(self):
        """Test BMR calculation with empty height."""
        self.assertIsNone(calculate_bmr("", 70, 25, "male"))
    
    def test_empty_weight_bmr(self):
        """Test BMR calculation with empty weight."""
        self.assertIsNone(calculate_bmr(175, "", 25, "male"))
    
    def test_empty_age_bmr(self):
        """Test BMR calculation with empty age."""
        self.assertIsNone(calculate_bmr(175, 70, "", "male"))
    
    def test_empty_gender_bmr(self):
        """Test BMR calculation with empty gender."""
        self.assertIsNone(calculate_bmr(175, 70, 25, ""))


class TestRequests(unittest.TestCase):
# Test for API

# Test for BMI endpoint

# Normal use case
    def test_bmi_endpoint_normal(self):
        response1 = base_request("bmi", {"height": 1.75, "weight": 70})
        response2 = base_request("bmi", {"height": 2, "weight": 100})
        response3 = base_request("bmi", {"height": 0.70, "weight": 10})
        
        print(response1)

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)

        self.assertAlmostEqual(response1.json()["data"]["bmi"], 22.86, places=2)
        self.assertAlmostEqual(response2.json()["data"]["bmi"], 25.00, places=2)
        self.assertAlmostEqual(response3.json()["data"]["bmi"], 20.41, places=2)

# Missing values
    def test_bmi_endpoint_missing_height(self):
        response = base_request("bmi", {"weight": 70})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Missing parameters: height")


    def test_bmi_endpoint_missing_weight(self):
        response = base_request("bmi", {"height": 1.75})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Missing parameters: weight")

# Incorrect values (zero, negative, empty strings)
    def test_bmi_endpoint_negative_height(self):
        response = base_request("bmi", {"height": -1.75, "weight": 70})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. Height and weight must be greater than 0")
    
    def test_bmi_endpoint_negative_weight(self):
        response = base_request("bmi", {"height": 1.75, "weight": -70})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. Height and weight must be greater than 0")
    
    def test_bmi_endpoint_zero_height(self):
        response = base_request("bmi", {"height": 0, "weight": 70})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. Height and weight must be greater than 0")
    
    def test_bmi_endpoint_zero_weight(self):
        response = base_request("bmi", {"height": 1.75, "weight": 0})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. Height and weight must be greater than 0")

    def test_bmi_endpoint_empty_height(self):
        response = base_request("bmi", {"height": "", "weight": 70})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. Height and weight must be greater than 0")
    
    def test_bmi_endpoint_empty_weight(self):
        response = base_request("bmi", {"height": 1.75, "weight": ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. Height and weight must be greater than 0")

# Test for BMR endpoint

# Normal use case
    def test_bmr_endpoint_normal_male(self):
        response = base_request("bmr", {"height": 175, "weight": 70, "age":25, "gender":"male"})
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(response.json()["data"]["bmr"], 1724.05, places=2)

    
    def test_bmr_endpoint_normal_female(self):
        response = base_request("bmr", {"height": 165, "weight": 60, "age":25, "gender":"female"})
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(response.json()["data"]["bmr"], 1405.33, places=2)

# Missing values
    def test_bmr_endpoint_missing_height(self):
        response = base_request("bmr", {"weight": 70, "age":25, "gender": "male"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Missing parameters: height")
    
    def test_bmr_endpoint_missing_weight(self):
        response = base_request("bmr", {"height": 175, "age": 25, "gender":"male"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Missing parameters: weight")
    
    def test_bmr_endpoint_missing_age(self):
        response = base_request("bmr", {"height": 175, "weight": 70, "gender": "male"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Missing parameters: age")

    def test_bmr_endpoint_missing_gender(self):
        response = base_request("bmr", {"height": 175, "weight": 70, "age": 25})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Missing parameters: gender")

# Incorrect values (zero, negative, empty strings, incorrect genders)
    def test_bmr_endpoint_negative_height(self):
        response = base_request("bmr", {"height": -175, "weight": 70, "age": 25, "gender": "male"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. The correct genders are male or female, height, weight and age must be greater than 0")
    
    def test_bmr_endpoint_negative_weight(self):
        response = base_request("bmr", {"height": 175, "weight": -70, "age": 25, "gender": "male"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. The correct genders are male or female, height, weight and age must be greater than 0")
    
    def test_bmr_endpoint_negative_age(self):
        response = base_request("bmr", {"height": 175, "weight": 70, "age": -25, "gender": "male"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. The correct genders are male or female, height, weight and age must be greater than 0") 

    def test_bmr_endpoint_incorrect_gender(self):
        response = base_request("bmr", {"height": 175, "weight": 70, "age": 25, "gender": "emale"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. The correct genders are male or female, height, weight and age must be greater than 0")
    
    def test_bmr_endpoint_zero_height(self):
        response = base_request("bmr", {"height": 0, "weight": 70, "age": 25, "gender": "male"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. The correct genders are male or female, height, weight and age must be greater than 0") 
    
    def test_bmr_endpoint_zero_weight(self):
        response = base_request("bmr", {"height": 175, "weight": 0, "age": 25, "gender": "male"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. The correct genders are male or female, height, weight and age must be greater than 0")
    
    def test_bmr_endpoint_zero_age(self):
        response = base_request("bmr", {"height": 175, "weight": 70, "age": 0, "gender": "male"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. The correct genders are male or female, height, weight and age must be greater than 0")
    
    def test_bmr_endpoint_empty_height(self):
        response = base_request("bmr", {"height": "", "weight": 70, "age": 0, "gender": "male"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. The correct genders are male or female, height, weight and age must be greater than 0")

    def test_bmr_endpoint_empty_weight(self):
        response = base_request("bmr", {"height": 175, "weight": "", "age": 25, "gender": "male" })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. The correct genders are male or female, height, weight and age must be greater than 0")

    def test_bmr_endpoint_empty_age(self):
        response = base_request("bmr", {"height": 175, "weight": 70, "age": "", "gender": "male"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. The correct genders are male or female, height, weight and age must be greater than 0")

    def test_bmr_endpoint_empty_gender(self):
        response = base_request("bmr", {"height": 175, "weight": 70, "age": 25, "gender": ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["metadata"]["message"], "Invalid request check your inputs. The correct genders are male or female, height, weight and age must be greater than 0")

if __name__ == "__main__":
    unittest.main(verbosity=2)