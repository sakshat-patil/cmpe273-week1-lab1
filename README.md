# cmpe273-week1-lab1

## How to Run Locally
Prerequisites
Python 3.10+

pip (Python package manager)

1. Install Dependencies
Open a terminal in the project directory and run:

Bash
pip install -r requirements.txt
2. Start the Services
You need to run each service in a separate terminal window.

Terminal 1 (Service A - Echo API):

Bash
python service_a.py
Runs on http://localhost:8080

Terminal 2 (Service B - Client):

Bash
python service_b.py
Runs on http://localhost:8081

## Success + Failure Proof
1. Success Case
Command:

Bash
curl "http://localhost:8081/call-echo?msg=hello"
Output:

JSON
{
  "original": {
    "echo": "hello"
  },
  "result": "Service B received response"
}
Service B Logs:

Plaintext
Service B | GET /call-echo | Status: 200 | Latency: 15.20ms

<img width="2940" height="1862" alt="image" src="https://github.com/user-attachments/assets/eae77142-cfcc-4db1-a969-8ca6d44a876c" />

2. Failure Case (Service A Down)
Steps:

Stop Service A by pressing Ctrl+C in Terminal 1.

Run the curl command again.

Command:

Bash
curl -v "http://localhost:8081/call-echo?msg=hello"
Output:

JSON
{
  "error": "Service A is unavailable"
}
(HTTP Status: 503 Service Unavailable)

<img width="2940" height="1912" alt="image" src="https://github.com/user-attachments/assets/2403de0f-9cf1-44a9-9614-47f80924e9c0" />


## What makes this distributed?
This system is distributed because the business logic is split into two independent processes (Service A and Service B) that run in their own memory spaces and communicate exclusively over a network protocol (HTTP). They do not share state or memory; Service B relies on Service A to complete its task, yet they have independent failure domains—if Service A crashes, Service B remains alive and can gracefully handle the failure (by returning a 503) rather than crashing itself.
