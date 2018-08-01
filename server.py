from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

from CertManager import CertManager
from MongoManager import MongoManager

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'fedssh'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/fedssh'

cm = CertManager()
mm = MongoManager(PyMongo(app))
FLASK_PORT = 6128

@app.route('/all_servers', methods=['GET'])
def get_all_servers():
    return jsonify({'servers': mm.get_all_servers()})

@app.route('/generate_cert', methods=['POST'])
def generate_cert():
    unique_name = request.json['name']
    #all_certs = (subprocess.run(['ls', CERTS_LOC])).stdout

    #star = mongo.db.stars
    """
    output = []
    for s in star.find():
        output.append({'name' : s['name'], 'distance' : s['distance']})
    return jsonify({'result' : output})
    """

@app.route('/generate_link_cert', methods=['POST'])
def generate_and_link_cert():
    unique_name = request.json['name']
    #all_certs = (subprocess.run(['ls', CERTS_LOC])).stdout

    #star = mongo.db.stars
    """
    output = []
    for s in star.find():
        output.append({'name' : s['name'], 'distance' : s['distance']})
    return jsonify({'result' : output})
    """

"""
@app.route('/star/', methods=['GET'])
def get_one_star(name):

    star = mongo.db.stars
    s = star.find_one({'name' : name})
    output = None
    if s:
        output = {'name' : s['name'], 'distance' : s['distance']}
    else:
        output = "No such name"
    return jsonify({'result' : output})

@app.route('/star', methods=['POST'])
def add_star():
    star = mongo.db.stars
    name = request.json['name']
    distance = request.json['distance']
    star_id = star.insert({'name': name, 'distance': distance})
    new_star = star.find_one({'_id': star_id })
    output = {'name' : new_star['name'], 'distance' : new_star['distance']}
    return jsonify({'result' : output})
"""

if __name__ == '__main__':
   #cm.add_cert('test')
   #mm.add_server('test@0.0.0.0', 'test_alias', 'test-servers')
   app.run(debug=True, port=FLASK_PORT)
