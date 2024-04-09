from flask import Flask, render_template, send_from_directory, request, make_response, session, jsonify
import json
import uuid
import base64 

app = Flask(__name__)

messages = {}

@app.route('/message', methods=['GET'])
def getMessageRoute():
	try:
		messageId = request.args.get('messageId')
		if not messageId:
			return 'Invalid Request', 400

		if not messages[messageId]:
			return 'Not Found', 404

		return jsonify({
			messageId: messageId,
			encryptedMessage: messages[messageId]
		}), 200
	except:
		return 'Invalid Request', 400

@app.route('/message', methods=['POST'])
def createMessageRoute():
	try:
		if not request.is_json:
			return 'Invalid Request', 400

		data = request.json
		
		callsign = data.get('callsign')
		message = data.get('message')

		if not callsign or not message:
			return 'Invalid Request', 400

		newID = str(uuid.uuid4())

		messages[newID] = """
	-----BEGIN PGP MESSAGE-----
	Version: Encryption Desktop 10.5.0 (Build 1180)
	Charset: utf-8
	{message}
	-----END PGP MESSAGE-----
	""".format(message=base64.b64encode(message.encode("ascii")).decode("ascii"))

		return jsonify({
			'messageId': newID,
			'encryptedMessage': messages[newID]
		}), 200
	except:
		return 'Invalid Request', 400

if __name__ == "__main__":
	app.run(debug=True)