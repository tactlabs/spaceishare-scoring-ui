'''
Created on 

Course work: 

@author: Harini

Source:
    
'''

# Import necessary modules
from flask import  Flask,render_template, send_file, request
from flask import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():

    return render_template('index.html')

@app.route('/', methods=['POST'])
def home_post():

    link = request.form.get('input')
    return render_template('index.html')

def startpy():

    app.run(debug=True)

if __name__ == '__main__':

    startpy()