from flask import Flask, render_template, request, redirect, url_for
import uuid
import requests

app = Flask(__name__)

# A simple in-memory database to store cases (in a real application, use a proper database)
cases = {}

# Function to perform WHOIS lookup using a free API
def whois_lookup(domain):
    response = requests.get(f"https://jsonwhoisapi.com/api/v1/whois?identifier={domain}",
                            headers={"Authorization": "Token ffsrgY1SxGtf-WwVvgTr6A"})
    return response.json()

# Function to perform IP geolocation using a free API
def ip_geolocation(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/request', methods=['GET', 'POST'])
def request_service():
    if request.method == 'POST':
        client_name = request.form['client_name']
        client_email = request.form['client_email']
        service_needed = request.form['service_needed']
        case_id = str(uuid.uuid4())
        
        cases[case_id] = {
            'client_name': client_name,
            'client_email': client_email,
            'service_needed': service_needed,
            'status': 'Pending'
        }
        
        return redirect(url_for('case_status', case_id=case_id))
    return render_template('request.html')

@app.route('/status/<case_id>')
def case_status(case_id):
    case = cases.get(case_id)
    if not case:
        return 'Case not found', 404
    return render_template('status.html', case=case, case_id=case_id)

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        query = request.form['query']
        service = request.form['service']
        
        if service == 'whois':
            result = whois_lookup(query)
        elif service == 'ip_geo':
            result = ip_geolocation(query)
        else:
            result = f"Unknown service: {service}"
        
        return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
