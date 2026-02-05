from flask import Flask, request, jsonify
import requests
import logging
import time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("ServiceB")

SERVICE_A_URL = "http://localhost:8080/echo"

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    if request.path != '/favicon.ico':
        latency = (time.time() - request.start_time) * 1000 # ms
        logger.info(f"Service B | {request.method} {request.path} | Status: {response.status_code} | Latency: {latency:.2f}ms")
    return response

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/call-echo', methods=['GET'])
def call_echo():
    msg = request.args.get('msg', '')
    
    try:
        # Call Service A with a timeout
        response = requests.get(SERVICE_A_URL, params={'msg': msg}, timeout=2.0)
        
        # If Service A returns a 4xx or 5xx error, raise an exception
        response.raise_for_status()
        
        data = response.json()
        return jsonify({"result": "Service B received response", "original": data})
        
    except requests.exceptions.RequestException as e:
        # Log the error clearly
        logger.error(f"Error calling Service A: {e}")
        # Return 503 Service Unavailable
        return jsonify({"error": "Service A is unavailable"}), 503

if __name__ == '__main__':
    # Run Service B on port 8081
    app.run(host='0.0.0.0', port=8081)