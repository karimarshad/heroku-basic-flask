from flask import Flask, render_template, request, jsonify
import json
import re
from flask_cors import CORS
from riskscore import calculate_framingham_score
from global_vars import onea_message, oneb_message, onec_message, oned_message, onee_message, onef_message, oneg_message
from global_vars import twoa_message, twob_message, twoc_message, twod_message, twoe_message, twof_message, twog_message
from global_vars import threea_message, threeb_message, threec_message, threed_message, threee_message, threef_message, threeg_message
from global_vars import foura_message, fourb_message, fourc_message, fourd_message, foure_message, fourf_message, fourg_message
from global_vars import fivea_message, fiveb_message, fivec_message, fived_message, fivee_message, fivef_message, fiveg_message
from global_vars import sixa_message, sixb_message, sixc_message, sixd_message, sixe_message, sixf_message, sixg_message

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
            #recommendations.append("Cascade Screening, FHF, General Cardiologist")
            recommendations.append(oneb_message)
        elif carotid_usg_result and fhg_test_result and lp_value >75: #1c
            recommendations.append(onec_message)
        elif carotid_usg_result and fhg_test_result and lp_value <75: #1d
            recommendations.append(oned_message)
        elif not carotid_usg_result and not fhg_test_result and lp_value >75: #1e
            recommendations.append(onee_message)
        elif carotid_usg_result and fhg_test_result and lp_value <75: #1f
            recommendations.append(onef_message)
        else:
            recommendations.append(oneg_message) #add code for onea_message
    elif ( 0 < cac_score < 10):
        if carotid_usg_result and not fhg_test_result and lp_value > 75: #2b
            recommendations.append(twob_message)
        elif carotid_usg_result and fhg_test_result and lp_value >75: #2c
            recommendations.append(twoc_message)
        elif carotid_usg_result and fhg_test_result and lp_value <75: #2d
            recommendations.append(twod_message)
        elif not carotid_usg_result and not fhg_test_result and lp_value >75: #2e
            recommendations.append(twoe_message)
        elif carotid_usg_result and fhg_test_result and lp_value <75: #2f
            recommendations.append(twof_message)
        else:
            recommendations.append(twog_message)    
    elif (10 < cac_score < 100):
        if carotid_usg_result and not fhg_test_result and lp_value > 75: #3b
            recommendations.append(threeb_message)
        elif carotid_usg_result and fhg_test_result and lp_value >75: #3c
            recommendations.append(threec_message)
        elif carotid_usg_result and fhg_test_result and lp_value <75: #3d
            recommendations.append(threed_message)
        elif not carotid_usg_result and not fhg_test_result and lp_value >75: #3e
            recommendations.append(threee_message)
        elif carotid_usg_result and fhg_test_result and lp_value <75: #3f
            recommendations.append(threef_message)
        else:
            recommendations.append("Lipid Lowering Therapy, Exercise Medicine and Nutritionist(rec 3a or 3g)") 
    elif (99 < cac_score < 400):
        if carotid_usg_result and not fhg_test_result and lp_value > 75: #4b
            recommendations.append(fourb_message)
        elif carotid_usg_result and fhg_test_result and lp_value >75: #4c
            recommendations.append(fourc_message)
        elif carotid_usg_result and fhg_test_result and lp_value <75: #4d
            recommendations.append(fourd_message)
        elif not carotid_usg_result and not fhg_test_result and lp_value >75: #4e
            recommendations.append(foure_message)
        elif carotid_usg_result and fhg_test_result and lp_value <75: #4f
            recommendations.append(fourf_message)
        else:
            recommendations.append(fourg_message) 
    elif (399 < cac_score < 1000):
        if carotid_usg_result and not fhg_test_result and lp_value > 75: #5b
            recommendations.append(fiveb_message)
        elif carotid_usg_result and fhg_test_result and lp_value >75: #5c
            recommendations.append(fivec_message)
        elif carotid_usg_result and fhg_test_result and lp_value <75: #5d
            recommendations.append(fived_message)
        elif not carotid_usg_result and not fhg_test_result and lp_value >75: #5e
            recommendations.append(fivee_message)
        elif carotid_usg_result and fhg_test_result and lp_value <75: #5f
            recommendations.append(fivef_message)
        else:
            recommendations.append(fiveg_message) 
    elif (cac_score > 999):
        if carotid_usg_result and not fhg_test_result and lp_value > 75: #6b
            recommendations.append(sixb_message)
        elif carotid_usg_result and fhg_test_result and lp_value >75: #6c
            recommendations.append(sixc_message)
        elif carotid_usg_result and fhg_test_result and lp_value <75: #6d
            recommendations.append(sixd_message)
        elif not carotid_usg_result and not fhg_test_result and lp_value >75: #6e
            recommendations.append(sixe_message)
        elif carotid_usg_result and fhg_test_result and lp_value <75: #6f
            recommendations.append(sixf_message)            
    # Add other score ranges similarly
    else:
        recommendations.append(sixg_message)

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
        recommendations = cad_reco + [f"Your Framingham Score is: {frg_score}", f"The % risk of having a cardiovascular disease in next 10 years is: {frg_risk_percentage}"]
        
        # Return the recommendation Summary to client
        return jsonify({"recommendations": recommendations})
    
        #return jsonify({"message": "GET method is not supported for this endpoint"})

@app.route('/')
def index():
#    return 'Hello, World!'
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    
