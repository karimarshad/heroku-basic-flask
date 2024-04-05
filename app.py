from flask import Flask, render_template, request, jsonify
import json
import re
from flask_cors import CORS
from riskscore import calculate_framingham_score

app = Flask(__name__)
#CORS(app)
CORS(app, origins='*')

def extract_numerical_value(conclusion):
    """Extracts numerical value from conclusion string."""
    match = re.search(r'\d+(\.\d+)?', conclusion)
    if match:
        return float(match.group())
    else:
        return None

def get_reports(clinic_data):
    """Extracts diagnostic reports from clinic data."""
    reports = {}
    for entry in clinic_data['entry']:
        if entry['resource']['resourceType'] == 'DiagnosticReport':
            report = entry['resource']
            reports[report['code']['coding'][0]['display']] = report['conclusion']
    return reports

def check_conditions(reports):
    """Checks input conditions and returns True if all conditions are met, otherwise returns False."""
    return ("Familial hypercholesterolemia genetic testing" in reports and 
            "Lipoprotein (a) [Mass/volume] in Serum or Plasma" in reports and 
            "Carotid arteries Duplex Ultrasound" in reports and 
            "Coronary Artery Calcium Score" in reports)

def convert_fhg_test_result(fhg_test_string):
    """Converts FHG test result string to boolean."""
    return fhg_test_string == "The genetic test indicates familial hypercholesterolemia."

def convert_carotid_usg_result(carotid_ultrasound_string):
    """Converts carotid ultrasound result string to boolean."""
    return "no plaque" not in carotid_ultrasound_string

def cad_recommendations(cac_score, carotid_usg_result, fhg_test_result, lp_value):
    """Recommends CAD management based on conditions."""
    recommendations = []
    if cac_score == 0:
        if carotid_usg_result and not fhg_test_result and lp_value > 75: #1b
            recommendations.append("Cascade Screening, FHF, General Cardiologist")
        elif carotid_usg_result and fhg_test_result and lp_value >75: #1c
            recommendations.append("Cascade Screening, FHF, General Cardiologist, and Genetic Screening")
        elif carotid_usg_result and fhg_test_result and lp_value <75: #1d
            recommendations.append("Cascade Screening, FHF, General Cardiologist, and Genetic Screening")
        elif not carotid_usg_result and not fhg_test_result and lp_value >75: #1e
            recommendations.append("Cascade Screening, FHF, General Cardiologist")
        elif carotid_usg_result and fhg_test_result and lp_value <75: #1f
            recommendations.append("Cascade Screening, FHF, General Cardiologist")
        else:
            recommendations.append("Lipid Lowering Therapy, Exercise Medicine and Nutritionist(rec 1a or 1g)")
    elif ( 0 < cac_score < 10):
        if carotid_usg_result and not fhg_test_result and lp_value > 75: #2b
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist 2b")
        elif carotid_usg_result and fhg_test_result and lp_value >75: #2c
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist, and Genetic Screening 2c")
        elif carotid_usg_result and fhg_test_result and lp_value <75: #2d
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist, and Genetic Screening 2d")
        elif not carotid_usg_result and not fhg_test_result and lp_value >75: #2e
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist 2e")
        elif carotid_usg_result and fhg_test_result and lp_value <75: #2f
            recommendations.append("Cascade Screening, FHF, General Cardiologist 2f")
        else:
            recommendations.append("Lipid Lowering Therapy, Exercise Medicine and Nutritionist(rec 2a or 2g)")    
    elif (10 < cac_score < 100):
        if carotid_usg_result and not fhg_test_result and lp_value > 75: #3b
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist 3b")
        elif carotid_usg_result and fhg_test_result and lp_value >75: #3c
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist, and Genetic Screening 3c")
        elif carotid_usg_result and fhg_test_result and lp_value <75: #3d
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist, and Genetic Screening 3d")
        elif not carotid_usg_result and not fhg_test_result and lp_value >75: #3e
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist 3e")
        elif carotid_usg_result and fhg_test_result and lp_value <75: #3f
            recommendations.append("Cascade Screening, FHF, General Cardiologist 3f")
        else:
            recommendations.append("Lipid Lowering Therapy, Exercise Medicine and Nutritionist(rec 3a or 3g)") 
    elif (99 < cac_score < 400):
        if carotid_usg_result and not fhg_test_result and lp_value > 75: #4b
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist 4b")
        elif carotid_usg_result and fhg_test_result and lp_value >75: #4c
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist, and Genetic Screening 4c")
        elif carotid_usg_result and fhg_test_result and lp_value <75: #4d
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist, and Genetic Screening 4d")
        elif not carotid_usg_result and not fhg_test_result and lp_value >75: #4e
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist 4e")
        elif carotid_usg_result and fhg_test_result and lp_value <75: #4f
            recommendations.append("Cascade Screening, FHF, General Cardiologist 4f")
        else:
            recommendations.append("Lipid Lowering Therapy, Exercise Medicine and Nutritionist(rec 5a or 5g)") 
    elif (399 < cac_score < 1000):
        if carotid_usg_result and not fhg_test_result and lp_value > 75: #5b
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist 5b")
        elif carotid_usg_result and fhg_test_result and lp_value >75: #5c
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist, and Genetic Screening 5c")
        elif carotid_usg_result and fhg_test_result and lp_value <75: #5d
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist, and Genetic Screening 5d")
        elif not carotid_usg_result and not fhg_test_result and lp_value >75: #5e
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist 5e")
        elif carotid_usg_result and fhg_test_result and lp_value <75: #5f
            recommendations.append("Cascade Screening, FHF, General Cardiologist 5f")
        else:
            recommendations.append("Lipid Lowering Therapy, Exercise Medicine and Nutritionist(rec 5a or 5g)") 
    elif (cac_score > 999):
        if carotid_usg_result and not fhg_test_result and lp_value > 75: #6b
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist 6b")
        elif carotid_usg_result and fhg_test_result and lp_value >75: #6c
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist, and Genetic Screening 6c")
        elif carotid_usg_result and fhg_test_result and lp_value <75: #6d
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist, and Genetic Screening 6d")
        elif not carotid_usg_result and not fhg_test_result and lp_value >75: #6e
            recommendations.append("Aspirin, Cascade Screening, FHF, General Cardiologist 6e")
        elif carotid_usg_result and fhg_test_result and lp_value <75: #6f
            recommendations.append("Cascade Screening, FHF, General Cardiologist 6f")            
    # Add other score ranges similarly
    else:
        recommendations.append("Lipid Lowering Therapy, Exercise Medicine and Nutritionist")

    return recommendations

@app.route('/recommendations', methods=['GET','POST'])
def get_recommendations():
    """Endpoint to receive JSON data and return recommendations."""
    if request.method == 'POST':
        req_data = request.get_json()
        clinic_data = req_data.get('clinic_data', {})
        reports = get_reports(clinic_data)
        if check_conditions(reports):
            fhg_test_result = convert_fhg_test_result(reports.get("Familial hypercholesterolemia genetic testing", ""))
            lp_value = extract_numerical_value(reports.get("Lipoprotein (a) [Mass/volume] in Serum or Plasma", ""))
            carotid_usg_result = convert_carotid_usg_result(reports.get("Carotid arteries Duplex Ultrasound", ""))
            cac_score = extract_numerical_value(reports.get("Coronary Artery Calcium Score", ""))
            recommendations = cad_recommendations(cac_score, carotid_usg_result, fhg_test_result, lp_value)
            return jsonify({"recommendations": recommendations})
        else:
            return jsonify({"error": "Insufficient data to make recommendations"})
    elif request.method == 'GET':
        # Handle GET request (if necessary)
        lp_value = float(request.args.get('lp_value', 0))
        carotid_usg_result = request.args.get('carotid_usg_result', '') == 'true'
        fhg_test_result = request.args.get('fhg_test_result', '') == 'true'
        cac_score = float(request.args.get('cac_score', 0))
        age = int(request.args.get('age',0))
        gender= request.args.get('gender',"male")
        total_chol = int(request.args.get('total_chol',0))
        is_smoker = request.args.get('is_smoker',0)
        hdl_chol = int(request.args.get('hdl_chol',0))
        systolic_bp = int(request.args.get('systolic_bp',0))
        treated = request.args.get('treated',0)
       
        #calculate framingham scoring
        frg_score, frg_risk_percentage = calculate_framingham_score(gender,age,total_chol,is_smoker,hdl_chol,systolic_bp,treated)
        

        # Generate Coronary recommendations
        cad_reco = cad_recommendations(cac_score, carotid_usg_result, fhg_test_result, lp_value)
        
        #Combine Framingham Scoring to the recommendations
        recommendations = cad_reco + [f"Framingham Score: {frg_score}", f"Framingham Risk %: {frg_risk_percentage}"]
        
        # Return the recommendation Summary to client
        return jsonify({"recommendations": recommendations})
    
        #return jsonify({"message": "GET method is not supported for this endpoint"})

@app.route('/')
def index():
#    return 'Hello, World!'
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    
