from flask import Flask, request, jsonify
import logging
import time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("ServiceA")

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    if request.path != '/favicon.ico':
        latency = (time.time() - request.start_time) * 1000 # ms
        logger.info(f"Service A | {request.method} {request.path} | Status: {response.status_code} | Latency: {latency:.2f}ms")
    return response

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/echo', methods=['GET'])
def echo():
    msg = request.args.get('msg', '')
    return jsonify({"echo": msg})

if __name__ == '__main__':
    # Run Service A on port 8080
    app.run(host='0.0.0.0', port=8080)