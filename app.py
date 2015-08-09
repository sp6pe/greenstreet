from flask import Flask, jsonify, render_template, redirect, request
import json
import twilio.twiml
from utils import connect_db
from validate_email import validate_email
from whitenoise import WhiteNoise

app = Flask(__name__) #establishing flask app
static = WhiteNoise(app, root='./static/')

def verify(email):
    is_valid = validate_email(email, verify = True)
    return is_valid

@app.route('/')
def index():
	return render_template('index.html')

@app.route("/received/", methods=['GET', 'POST'])
def receive_message():
    sender = request.values.get('From',None)
    db = connect_db('MONGOHQ_URL', 'MONGO_DATABASE_NAME')
    user = db.users.find_one({"number":sender})
    message = request.values.get('Body',None)
    resp = twilio.twiml.Response()
    
    if user != None:
    	try:
    		email = user['email']
    	except KeyError:
    		is_valid = verify(message)
    		if is_valid or is_valid == None:
    			db.users.update_one({
				  '_id': user['_id']
				},{
				  '$set': {
				    'email': message
				  }
				}, upsert=False)
    			resp.message("Thank you! You've been added to the waitlist. As soon as we can work through our current orders, we'll be in touch!")
    		else:
    			resp.message("Please send us a valid email address!")
    	else:
    		resp.message("You are currently on the waitlist. We will contact you shortly!")
    else:
    	"""Respond to incoming calls with a simple text message."""
    	resp.message("Welcome to Green Street! To get started, please send us your email address. We will only use it to send you order confirmations, receipts, and updates.")
    	db.users.insert({"number":sender})
    return str(resp)

if __name__ == "__main__":
	app.run(debug = True)



