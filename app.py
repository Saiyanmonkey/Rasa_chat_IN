from email import message
from urllib import response
from flask import Flask, render_template, request, jsonify
import os, sys, requests, json
from random import randint

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello Worlds!</h1>'

@app.route('/parse', methods=['POST'])
def extract():
    text = str(request.form['value1'])
    payload = json.dumps({"sender":"Customer","message":text})
    headers = {'Content-type': 'application/json', 'Accept':     'text/plain'}
    response = requests.request("POST",   url="http://localhost:5005/webhooks/rest/webhook", headers=headers, data=payload)
    response = response.json()
    resp = []
    for i in range(len(response)):
        try:
            resp.append(response[i]['text'])
        except:
            continue
    result = resp  
    return jsonify(sender = "Rasa ", message=result)

if __name__=="__main__":
    app.run(debug=True)
