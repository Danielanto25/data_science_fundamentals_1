from flask import Flask
from flask import jsonify
import csv 

filename =  'iris.csv'
raw_data = open(filename , 'r')
reader = csv.reader(raw_data , delimiter=',',quoting=csv.QUOTE_NONE)
x = list(reader)


app = Flask(__name__)

@app.route('/')
def get_current_user():
    return jsonify(username="Maria",
                   email="maria@gmail.com",
                   id="1298")

@app.route('/json_from_tuple')
def show_tuple():
    return jsonify(1,2,3)

@app.route('/json_from_list')
def show_list():
    return jsonify(x)

if __name__ == '__main__':
    app.run()