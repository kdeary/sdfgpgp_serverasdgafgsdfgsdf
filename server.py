
from flask import Flask, render_template, send_from_directory, request, make_response, session, jsonify
import os
import gnupg
import json
import uuid
import base64 

app = Flask(__name__)

messages = {}

gpg = gnupg.GPG()

gpg.import_keys(open('mouse.asc').read())
gpg.import_keys(open('firefly.asc').read())
gpg.import_keys(open('goose.asc').read())

list_keys = gpg.list_keys()

# print(list_keys[0]['fingerprint'])

users = {
	"mouse": list_keys[0]['fingerprint'],
	"firefly": list_keys[1]['fingerprint'],
	"goose": list_keys[2]['fingerprint'],
}

@app.route('/message', methods=['GET'])
def getMessageRoute():
	messageId = request.args.get('messageId')
	print(messageId)

	if messageId is None:
		return 'Invalid Request', 400

	if not messageId in messages:
		return 'Not Found', 404

	print('??', messages[messageId])
	return jsonify({
		"messageId": messageId,
		"encryptedMessage": messages[messageId]
	}), 200

@app.route('/message', methods=['POST'])
def createMessageRoute():
	if not request.is_json:
		return 'Invalid Request', 400

	data = request.json

	print(data)
	
	callsign = data.get('callsign')
	message = data.get('message')

	print(callsign, message)

	if not callsign or not message:
		return 'Invalid Request', 400

	if not callsign in users:
		return 'Not Found', 404

	newID = str(uuid.uuid4())

	enc = gpg.encrypt(message, users[callsign], always_trust=True)
	messages[newID] = str(enc)

	print(enc.status)
	print(enc.stderr)

	if not enc.ok:
		return 'Invalid Request', 400

	return jsonify({
		"messageId": newID,
		"encryptedMessage": messages[newID]
	}), 200

if __name__ == "__main__":
	app.run(debug=True)