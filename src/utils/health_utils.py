def calculate_bmi(height, weight):
  try:
    # As those cases are not possible in real life the calculations won't even be done and the handler will return a 400 error
    if height is None or weight is None or height <= 0 or weight <= 0:
      return None

    return weight / (height ** 2)

  # If there is any kind of error during the calculation we return None and the handler will return a 400 error
  except Exception:
    return None

def calculate_bmr(height, weight, age, gender):

  try:
    if height is None or weight is None or age is None or height <= 0 or weight <= 0 or age <= 0:
      return None
    if gender == "male":
      return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    
    if gender == "female":
      return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age) 

  # Invalid gender in parameter the function will return None and the api will return a 400 error
    return None

  except Exception:
    return None
