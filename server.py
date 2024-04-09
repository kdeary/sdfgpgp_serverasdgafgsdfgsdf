from flask import Flask, render_template, send_from_directory, request, make_response, session, jsonify
import json
import uuid
import base64 

app = Flask(__name__)

messages = {}

gpg = gnupg.GPG()
input_data = gpg.gen_key_input(
    name_email='testgpguser@mydomain.com',
    passphrase='my passphrase')
key = gpg.gen_key(input_data)
print(key)

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
	try:
		if not request.is_json:
			return 'Invalid Request', 400

		data = request.json

		print(data)
		
		callsign = data.get('callsign')
		message = data.get('message')

		if not callsign or not message:
			return 'Invalid Request', 400

		newID = str(uuid.uuid4())

		enc = gpg.encrypt(message, 'testgpguser@mydomain.com')
		messages[newID] = str(enc)

		if not enc.ok:
			return 'Invalid Request', 400

		return jsonify({
			"messageId": newID,
			"encryptedMessage": messages[newID]
		}), 200
	except Exception as err:
		print(err)
		return 'Invalid Request', 400

if __name__ == "__main__":
	app.run(debug=True)