import json
import math

def calculate_framingham_score(gender, age, total_chol, is_smoker, hdl_chol, systolic_bp, treated=False):
    # Age points
    age_points = 0 
    age = int(age)
    if gender == 'female':
        if 20 <= age <= 34:
            age_points = -7
        elif 35 <= age <= 39:
            age_points = -3
        elif 40 <= age <= 44:
            age_points = 0
        elif 45 <= age <= 49:
            age_points = 3
        elif 50 <= age <= 54:
            age_points = 6
        elif 55 <= age <= 59:
            age_points = 8
        elif 60 <= age <= 64:
            age_points = 10
        elif 65 <= age <= 69:
            age_points = 12
        elif 70 <= age <= 74:
            age_points = 14
        elif 75 <= age <= 79:
            age_points = 16
    else:  # male
        if 20 <= age <= 34:
            age_points = -9
        elif 35 <= age <= 39:
            age_points = -4
        elif 40 <= age <= 44:
            age_points = 0
        elif 45 <= age <= 49:
            age_points = 3
        elif 50 <= age <= 54:
            age_points = 6
        elif 55 <= age <= 59:
            age_points = 8
        elif 60 <= age <= 64:
            age_points = 10
        elif 65 <= age <= 69:
            age_points = 11
        elif 70 <= age <= 74:
            age_points = 12
        elif 75 <= age <= 79:
            age_points = 13

    # Total Cholesterol points
    total_chol_points = 0
    if gender == 'female':
        if age < 40:
            if total_chol < 160:
                total_chol_points = 0
            elif 160 <= total_chol <= 199:
                total_chol_points = 4
            elif 200 <= total_chol <= 239:
                total_chol_points = 8
            elif 240 <= total_chol <= 279:
                total_chol_points = 11
            else:
                total_chol_points = 13
        elif 40 <= age < 50:
            if total_chol < 160:
                total_chol_points = 0
            elif 160 <= total_chol <= 199:
                total_chol_points = 3
            elif 200 <= total_chol <= 239:
                total_chol_points = 6
            elif 240 <= total_chol <= 279:
                total_chol_points = 8
            else:
                total_chol_points = 10
        elif 50 <= age < 60:
            if total_chol < 160:
                total_chol_points = 0
            elif 160 <= total_chol <= 199:
                total_chol_points = 2
            elif 200 <= total_chol <= 239:
                total_chol_points = 4
            elif 240 <= total_chol <= 279:
                total_chol_points = 5
            else:
                total_chol_points = 7
        elif 60 <= age < 70:
            if total_chol < 160:
                total_chol_points = 0
            elif 160 <= total_chol <= 199:
                total_chol_points = 1
            elif 200 <= total_chol <= 239:
                total_chol_points = 2
            elif 240 <= total_chol <= 279:
                total_chol_points = 3
            else:
                total_chol_points = 4
        else:  # age >= 70
            if total_chol < 160:
                total_chol_points = 0
            elif 160 <= total_chol <= 199:
                total_chol_points = 1
            elif 200 <= total_chol <= 239:
                total_chol_points = 1
            elif 240 <= total_chol <= 279:
                total_chol_points = 2
            else:
                total_chol_points = 2
    else:  # male
        if age < 40:
            if total_chol < 160:
                total_chol_points = 0
            elif 160 <= total_chol <= 199:
                total_chol_points = 4
            elif 200 <= total_chol <= 239:
                total_chol_points = 7
            elif 240 <= total_chol <= 279:
                total_chol_points = 9
            else:
                total_chol_points = 11
        elif 40 <= age < 50:
            if total_chol < 160:
                total_chol_points = 0
            elif 160 <= total_chol <= 199:
                total_chol_points = 3
            elif 200 <= total_chol <= 239:
                total_chol_points = 5
            elif 240 <= total_chol <= 279:
                total_chol_points = 6
            else:
                total_chol_points = 8
        elif 50 <= age < 60:
            if total_chol < 160:
                total_chol_points = 0
            elif 160 <= total_chol <= 199:
                total_chol_points = 2
            elif 200 <= total_chol <= 239:
                total_chol_points = 3
            elif 240 <= total_chol <= 279:
                total_chol_points = 4
            else:
                total_chol_points = 5
        elif 60 <= age < 70:
            if total_chol < 160:
                total_chol_points = 0
            elif 160 <= total_chol <= 199:
                total_chol_points = 1
            elif 200 <= total_chol <= 239:
                total_chol_points = 1
            elif 240 <= total_chol <= 279:
                total_chol_points = 2
            else:
                total_chol_points = 3
        else:  # age >= 70
            if total_chol < 160:
                total_chol_points = 0
            elif 160 <= total_chol <= 199:
                total_chol_points = 0
            elif 200 <= total_chol <= 239:
                total_chol_points = 0
            elif 240 <= total_chol <= 279:
                total_chol_points = 1
            else:
                total_chol_points = 1

    # Smoking points
    smoking_points = 0
    if is_smoker:
        if gender == 'female':
            if 20 <= age < 40:
                smoking_points = 9
            elif 40 <= age < 50:
                smoking_points = 7
            elif 50 <= age < 60:
                smoking_points = 4
            elif 60 <= age < 70:
                smoking_points = 2
            else:  # age >= 70
                smoking_points = 1
        else:  # male
            if 20 <= age < 40:
                smoking_points = 8
            elif 40 <= age < 50:
                smoking_points = 5
            elif 50 <= age < 60:
                smoking_points = 3
            elif 60 <= age < 70:
                smoking_points = 1
            else:  # age >= 70
                smoking_points = 1
    else:
        smoking_points = 0

    # HDL cholesterol points
    hdl_chol = int(hdl_chol)
    if hdl_chol >= 60:
        hdl_chol_points = -1
    elif 50 <= hdl_chol <= 59:
        hdl_chol_points = 0
    elif 40 <= hdl_chol <= 49:
        hdl_chol_points = 1
    else:
        hdl_chol_points = 2

    # Systolic blood pressure points
    if treated:
        if systolic_bp < 120:
            systolic_bp_points = 0
        elif 120 <= systolic_bp < 130:
            systolic_bp_points = 3
        elif 130 <= systolic_bp < 140:
            systolic_bp_points = 4
        elif 140 <= systolic_bp < 160:
            systolic_bp_points = 5
        else:
            systolic_bp_points = 6
    else:
        if systolic_bp < 120:
            systolic_bp_points = 0
        elif 120 <= systolic_bp < 130:
            systolic_bp_points = 1
        elif 130 <= systolic_bp < 140:
            systolic_bp_points = 2
        elif 140 <= systolic_bp < 160:
            systolic_bp_points = 3
        else:
            systolic_bp_points = 4

    # Calculate total points
    total_points = age_points + total_chol_points + smoking_points + hdl_chol_points + systolic_bp_points

    # Calculate 10-year risk in %
    if gender == 'female':
        if total_points < 9:
            risk_percentage = "<1%"
        elif 9 <= total_points <= 12:
            risk_percentage = "1%"
        elif 13 <= total_points <= 14:
            risk_percentage = "2%"
        elif total_points == 15:
            risk_percentage = "3%"
        elif total_points == 16:
            risk_percentage = "4%"
        elif total_points == 17:
            risk_percentage = "5%"
        elif total_points == 18:
            risk_percentage = "6%"
        elif total_points == 19:
            risk_percentage = "8%"
        elif total_points == 20:
            risk_percentage = "11%"
        elif total_points == 21:
            risk_percentage = "14%"
        elif total_points == 22:
            risk_percentage = "17%"
        elif total_points == 23:
            risk_percentage = "22%"
        elif total_points == 24:
            risk_percentage = "27%"
        else:
            risk_percentage = "Over 30%"
    else:  # male
        if total_points == 0:
            risk_percentage = "<1%"
        elif 1 <= total_points <= 4:
            risk_percentage = "1%"
        elif 5 <= total_points <= 6:
            risk_percentage = "2%"
        elif total_points == 7:
            risk_percentage = "3%"
        elif total_points == 8:
            risk_percentage = "4%"
        elif total_points == 9:
            risk_percentage = "5%"
        elif total_points == 10:
            risk_percentage = "6%"
        elif total_points == 11:
            risk_percentage = "8%"
        elif total_points == 12:
            risk_percentage = "10%"
        elif total_points == 13:
            risk_percentage = "12%"
        elif total_points == 14:
            risk_percentage = "16%"
        elif total_points == 15:
            risk_percentage = "20%"
        elif total_points == 16:
            risk_percentage = "25%"
        else:
            risk_percentage = "Over 30%"

    return total_points, risk_percentage

# Example usage:
#gender = 'male'
#age = 45
#total_chol = 220
#is_smoker = True
#hdl_chol = 50
#systolic_bp = 140
#treated = False
def calculate_mesa_score(age, gender, race, total_chol, hdl_chol, systolic_bp, is_smoker, diabetes):
    # Coefficients for the MESA Risk Score
    coefficients = {
        "age_male": [9.124],  # Age coefficients for males
        "age_female": [7.209],  # Age coefficients for females
        "ln_totchol": [1.209],  # Natural logarithm of total cholesterol coefficient
        "ln_hdlchol": [-0.708],  # Natural logarithm of HDL cholesterol coefficient
        "ln_sysbp": [0.859],  # Natural logarithm of systolic blood pressure coefficient
        "is_smoker": [0.676],  # Smoker coefficient
        "is_diabetic": [0.658],  # Diabetes coefficient
        "race": {  # Race coefficients
            "White": 0,
            "Chinese": -0.576,
            "Black": 0.518,
            "Hispanic": 0.330
        },
        "intercept": -29.799  # Intercept
    }

    # Assign coefficients based on gender
    if gender == "male":
        coef_age = coefficients["age_male"][0]
    else:  # female
        coef_age = coefficients["age_female"][0]

    # Assign race coefficient
    coef_race = coefficients["race"][race]

    # Calculate MESA score
    score = coefficients["intercept"]
    print("coefficients:",coefficients["intercept"])
    score += coef_age * age
    score += coefficients["ln_totchol"][0] * math.log(total_chol)
    score += coefficients["ln_hdlchol"][0] * math.log(hdl_chol)
    score += coefficients["ln_sysbp"][0] * math.log(systolic_bp)
    score += coefficients["is_smoker"][0] * is_smoker
    score += coefficients["is_diabetic"][0] * diabetes
    score += coef_race

    # Convert score to risk percentage
    print(score)
    risk_percentage = 1 - (0.9533 ** math.exp(score - coefficients["intercept"]))

    return risk_percentage


def interpret_risk(score):
    if score < 10:
        return "Low risk (Less than 10% chance of developing CAD in the next 10 years)"
    elif 10 <= score < 20:
        return "Intermediate risk (10-20% chance of developing CAD in the next 10 years)"
    else:
        return "High risk (More than 20% chance of developing CAD in the next 10 years)"



# Read input parameters from JSON file
with open('patient_profile.json') as f:
    bundle_data = json.load(f)

# Find the Patient resource in the Bundle
patient_data = None
for entry in bundle_data.get('entry', []):
    resource = entry.get('resource', {})
    if resource.get('resourceType') == 'Patient':
        patient_data = resource
        print(patient_data['gender'])
        print(patient_data['birthDate'])
        break

# Extract age from birthDate if available
if patient_data and 'birthDate' in patient_data:
    birth_year = int(patient_data['birthDate'].split('-')[0])
    current_year = 2024  # Update with the current year
    age = current_year - birth_year
else:
    age = None
print(age)
# Extract gender if available
if patient_data and 'gender' in patient_data:
    gender = patient_data['gender']
else:
    gender = None

# Extract other parameters if available, or set them to None
#print(patient_data)
total_chol = bundle_data.get('total_chol')
hdl_chol = bundle_data.get('hdl_chol')
systolic_bp = bundle_data.get('systolic_bp')
is_smoker = bundle_data.get('is_smoker')
race = bundle_data.get('race')
diabetes = bundle_data.get('diabetes')
treated = False

# Check if required parameters are missing
if age is None or gender is None or total_chol is None or hdl_chol is None or systolic_bp is None or is_smoker is None:
    print("Error: Required parameters are missing in the patient data.")
else:
    total_points, risk_percentage = calculate_framingham_score(gender, age, total_chol, is_smoker, hdl_chol, systolic_bp, treated)
    print("Total Cholesterol :",total_chol)
    print("HDL Cholesterol :", hdl_chol)
    print("Systolic BP :", systolic_bp)
    print("Is Smoker :", is_smoker)
    print("Is Treated :", treated)
    print("Framingham Risk Score :", total_points)
    print("Race :", race)
    print ("Diabetic :", diabetes)
    print("10-Year Risk of Developing Coronary Heart Disease :", risk_percentage)
    mesa_score = calculate_mesa_score(age, gender, race, total_chol, hdl_chol, systolic_bp, is_smoker, diabetes)
    print("MESA Risk Score (10-Year Risk of Coronary Heart Disease events): {:.2%}".format(mesa_score))
