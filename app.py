from flask import Flask, jsonify, render_template, redirect, request
import json
import twilio.twiml
from utils import connect_db
from validate_email import validate_email


def verify(email):
	is_valid = validate_email(email, verify = True)
	return is_valid


app = Flask(__name__) #establishing flask app

@app.route('/')
def index():
	return render_template('index.html')

@app.route("/received/", methods=['GET', 'POST'])
def hello_monkey():
    sender = request.values.get('From',None)
    db = connect_db('MONGOHQ_URL', 'MONGO_DATABASE_NAME')
    user = db.users.find_one({"number":sender})
    message = request.values.get('Body',None)
    resp = twilio.twiml.Response()
    
    print sender 
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
    			resp.message("Thank you, we have added you to the waitlist. We will contact you shortly")
    		else:
    			resp.message("Please send me us a valid email address. I need it to send you order confirmations, receipts, etc.")
    	else:
    		resp.message("You are currently on the waitlist. We will contact you shortly")
    else:
    	"""Respond to incoming calls with a simple text message."""
    	resp.message("Hi There! To get started, please send me your email address. I need it to send you order confirmations, receipts, etc.")
    	db.users.insert({"number":sender})


    return str(resp)




if __name__ == "__main__":
	app.run(debug = True)



