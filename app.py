from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import boto3

app = Flask(__name__)
CORS(app)

s3 = boto3.client('s3',
                    aws_access_key_id='put-id-here',
                    aws_secret_access_key='put-key-here'
                      )
# s3 = boto3.client('s3')
BUCKET_NAME='lambda-s3-hs'

# Define key through env
#
# ACCESS_KEY_ID = asq
# ACCESS_SECRET_KEY = 
# AWS_SESSION_TOKEN = 

# dynamodb = boto3.resource('dynamodb',
#                     aws_access_key_id=ACCESS_KEY_ID,
#                     aws_secret_access_key=ACCESS_SECRET_KEY,
#                     aws_session_token=AWS_SESSION_TOKEN)

@app.route('/signup', methods=['post'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        try:
            table = dynamodb.Table('users')
            
            table.put_item(
                Item={
                    'name': name,
                    'email': email,
                    'password': password
                }
            )
        
            return jsonify({
                'name': name, 
                'email': email, 
                'password': password, 
                'status' : "SUCCESS",
                'msg': "Account successfully created"
            })
            # Success, prompt user to login platform
        except:
            return jsonify({
                'status': "FAILURE",
                'msg': "Error creating user"
            })

@app.route('/signin',methods = ['post'])
def check():
    if request.method=='POST':
        
        email = request.form['email']
        password = request.form['password']
        
        try:
            table = dynamodb.Table('users')
            response = table.query(
                    KeyConditionExpression=Key('email').eq(email)
            )
            items = response['Items']
            if (len(items) == 0):
                return ({
                    'status': "FAILURE",
                    'msg': "No user with such email found"
                })
            name = items[0]['name']
            
            if password == items[0]['password']:
                return jsonify({
                    'name': name,
                    'email': email,
                    'status': "SUCCESS",
                    'msg': "Sign in successful",
                })
                # Redirect to homepage
            else:
                return ({
                    'status': "FAILURE",
                    'msg': "Incorrect password"
                })
        except:
            return ({
                    'status': "FAILURE",
                    'msg': "Sign in error"
                })


@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        doc = request.files['file']
        if doc:
            try:
                filename = secure_filename(doc.filename)
                doc.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )

                return jsonify ({
                    'status': "SUCCESS",
                    'msg': "File upload to S3 successfully"
                })

            except:
                return jsonify ({
                    'status': "FAILURE",
                    'msg': "File upload error"
                })
                
