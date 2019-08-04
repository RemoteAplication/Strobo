from flask import (
        redirect, render_template, request, session, url_for, Flask,jsonify
)

import json
import bson
from pymongo import MongoClient
from flask_httpauth import HTTPBasicAuth
from bson.objectid import ObjectId

from pprint import pprint

# --- Mongodb --- #
client = MongoClient('mongodb://localhost:27017/')
db = client.RemoteApplication
Institute = db.Institute
Board = db.Board
Actuator = db.Actuator
Component = db.Component
Experiment = db.Experiment
Feature = db.Feature
People = db.People
Request = db.Request
Sensor = db.Sensor
Event = db.Event
Quiz = db.Quiz

application = Flask(__name__)
auth = HTTPBasicAuth()

# set the secret key.  keep this really secret:
application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@application.route("/")
def index():
    return render_template('index.html')

@application.route("/index.html")
def home():
    return render_template('index.html')

@application.route("/Experimento.html")
def Experimento():
    return render_template('Experimento.html')

@application.route("/FAQ.html")
def FAQ():
    return render_template('FAQ.html')

@application.route("/Sugestoes.html")
def Sugestoes():
    return render_template('Sugestoes.html')

@application.route("/experimento_strobo.html")
def experimento_strobo():
    return render_template('experimento_strobo.html')

@application.route("/teoria.html")
def teoria():
    return render_template('teoria.html')

#-- oAuth Operations --#
@auth.get_password
def get_pw(username):

    user = People.find_one({"login":username})
    if user is not None:
        return user['password']
    return None

### Institute Operations ###

def jsonInstitute(IT):
    missing = []

    if len(IT) == 0:
        return jsonify({'missing': 'json null'}), 404
    if not IT:
        return jsonify({'missing': 'json data'}), 400
    if ('name' in IT and IT['name'] == '') or (isinstance(IT['name'],str) != True) :
        missing.append('name')
    if 'initials' in IT and IT['initials'] == '':
        missing.append('initials')
    if 'address' in IT and IT['address'] == '':
        missing.append('address')
    if 'city' in IT and IT['city'] == '':
        missing.append('city')
    if 'state' in IT and IT['state'] == '':
        missing.append('state')
    if 'CEP' in IT and IT['CEP'] == '':
        missing.append('CEP')
    return(missing)

@application.route('/UpdateInstitute', methods=['POST'])
@auth.login_required
def UpdateInstitute():
    IT = request.json
    missing = []
    json_update = {}

    if ('name' in IT and IT['name'] == '') or (isinstance(IT['name'],str) != True) :
        missing.append('name')

    if missing == []:
        if 'newname' in IT and IT['newname'] != '':
            json_update['name']=IT['newname']
        if 'initials' in IT and IT['initials'] != '':
            json_update['initials']=IT['initials']
        if 'address' in IT and IT['address'] != '':
            json_update['address']=IT['address']
        if 'city' in IT and IT['city'] != '':
            json_update['city']=IT['city']
        if 'state' in IT and IT['state'] != '':
            json_update['state']=IT['state']
        if 'CEP' in IT and IT['CEP'] != '':
            json_update['CEP']=IT['CEP']
        if len(json_update) != 0:
            document = Institute.find_one_and_update({"name": IT['name']}, {"$set": json_update}, upsert=False)
        else:
            return jsonify({'missing': 'all components'}), 400
        if document is not None:
            return jsonify({'name': IT['name']}), 200
        else:
            return jsonify({'invalid': IT['name']}), 400
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ReadOneInstitute', methods=['GET'])
@auth.login_required
def ReadInstitute_one():
    IT = []
    name = request.args.get('name', default=1, type = str)
    if name == '':
        return jsonify({'missing':'name'}), 400
    else:
        doc = Institute.find_one({"name": name})
        if doc is not None:
            IT.append({'name': doc["name"], 'initials': doc["initials"], 'address': doc["address"], 'city': doc["city"],
                       'state': doc["state"], 'CEP': doc["CEP"]})
            return jsonify(IT), 200
        else:
            return jsonify({'invalid': name}),400

@application.route('/InsInstitute', methods=['POST','GET'])
def InsInstitute():
    IT = request.json
    missing = jsonInstitute(IT)

    if ('name' in IT and IT['name'] == '') or (isinstance(IT['name'], str) != True):
        missing.append('name')
    if missing == []:
        name = IT['name']
        initials = IT['initials']
        address = IT['address']
        city = IT['city']
        state = IT['state']
        CEP = IT['CEP']

        Institute.insert_one({"name": name, "initials": initials, "address": address, "city": city, "state": state, "CEP": CEP})

        return jsonify({'name': name}),200

    else:
        return jsonify({'missing': missing}),400

@application.route('/ListInstitute', methods=['GET'])
@auth.login_required
def ListInstitute():
    IT = []
    cursor = Institute.find({})

    for document in cursor:
        IT.append({'name': document["name"], 'initials': document["initials"], 'address': document["address"],'city': document["city"], 'state': document["state"], 'CEP': document["CEP"]})
    session['IT'] = IT

    return jsonify(IT),200

### Board Operations ###

def jsonBoard(BO):
    missing = []
    if len(BO) == 0:
        return jsonify({'missing': 'json null'}), 404
    if not BO:
        return jsonify({'missing': 'json data'}), 400
    if ('name' in BO and BO['name'] == '') or (isinstance(BO['name'], str) != True):
        missing.append('name')
    if 'tradeMark' in BO and BO['tradeMark'] == '':
        missing.append('tradeMark')
    if 'Model' in BO and BO['Model'] == '':
        missing.append('Model')
    if 'GPIO' in BO and BO['GPIO'] == '':
        missing.append('GPIO')
    if 'feature_id' in BO and BO['feature_id'] == '':
        missing.append('feature_id')
    if 'sensor_id' in BO and BO['sensor_id'] == '':
        missing.append('sensor_id')
    if 'actuator_id' in BO and BO['actuator_id'] == '':
        missing.append('actuator_id')

    return (missing)

@application.route('/UpdateBoard', methods=['POST'])
@auth.login_required
def UpdateBoard():
    BO = request.json
    missing = []
    json_update = {}

    if ('name' in BO and BO['name'] == '') or (isinstance(BO['name'], str) != True):
        missing.append('name')

    if missing == []:
        if (BO['feature_id'] != "") and (bson.objectid.ObjectId.is_valid(BO['feature_id']) == False) or\
            (BO['sensor_id'] != "") and (bson.objectid.ObjectId.is_valid(BO['sensor_id']) == False) or\
            (BO['actuator_id'] != "") and (bson.objectid.ObjectId.is_valid(BO['actuator_id']) == False):
            return jsonify({'invalid': 'ObjectID'}), 400
        if (BO['feature_id'] != "") and (Feature.find_one({"_id": ObjectId(BO['feature_id'])})) is None:
            return jsonify({'invalid': BO['feature_id']}), 400
        if (BO['sensor_id'] != "") and (Sensor.find_one({"_id": ObjectId(BO['sensor_id'])})) is None:
            return jsonify({'invalid': BO['sensor_id']}), 400
        if (BO['actuator_id'] != "") and (Actuator.find_one({"_id": ObjectId(BO['actuator_id'])})) is None:
            return jsonify({'invalid': BO['actuator_id']}), 400

        if 'newname' in BO and BO['newname'] != '':
            json_update['name']=BO['newname']
        if 'tradeMark' in BO and BO['tradeMark'] != '':
            json_update['tradeMark'] = BO['tradeMark']
        if 'Model' in BO and BO['Model'] != '':
            json_update['Model'] = BO['Model']
        if 'GPIO' in BO and BO['GPIO'] != '':
            json_update['GPIO'] = BO['GPIO']
        if 'feature_id' in BO and BO['feature_id'] != '':
            json_update['feature_id'] = BO['feature_id']
        if 'sensor_id' in BO and BO['sensor_id'] != '':
            json_update['sensor_id'] = BO['sensor_id']
        if 'actuator_id' in BO and BO['actuator_id'] != '':
            json_update['actuator_id'] = BO['actuator_id']

        if len(json_update)!=0 :
            if Board.find_one({"name": BO['newname']}) is not None:
                return jsonify({'duplicated': BO['newname']}), 400
            else:
                document = Board.find_one_and_update({"name": BO['name']}, {"$set": json_update}, upsert=False)
        else:
            return jsonify({'missing': 'all components'}), 400
        if document is not None:
            return jsonify({'name': BO['name']}), 200
        else:
            return jsonify({'invalid': BO['name']}), 400
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ReadOneBoard')
@auth.login_required
def ReadBoard_one():
    BO = []
    name = request.args.get('name', default=1, type=str)
    if name == '':
        return jsonify({'error': 'name'}), 400
    else:
        doc = Board.find_one({"name": name})
        if doc is not None:
            BO.append({'name': doc["name"], 'tradeMark': doc["tradeMark"], 'Model': doc["Model"], 'GPIO': doc["GPIO"],
                       'feature_id': doc["feature_id"], 'sensor_id': doc["sensor_id"],
                       'actuator_id': doc["actuator_id"]})
            return jsonify(BO), 200
        else:
            return jsonify({'invalid': name}),400

@application.route('/InsertBoard',methods=['POST'])
@auth.login_required
def InsertBoard():
    BO = request.json
    missing = jsonBoard(BO)

    if missing == []:

        if (bson.objectid.ObjectId.is_valid(BO['feature_id']) == False)  or\
            (bson.objectid.ObjectId.is_valid(BO['sensor_id']) == False) or\
            (bson.objectid.ObjectId.is_valid(BO['actuator_id']) == False):
            return jsonify({'invalid': 'ObjectID'}), 400
        if Feature.find_one({"_id": ObjectId(BO['feature_id'])}) is None:
            return jsonify({'invalid': BO['feature_id']}), 400
        if Sensor.find_one({"_id": ObjectId(BO['sensor_id'])}) is None:
            return jsonify({'invalid': BO['sensor_id']}), 400
        if  Actuator.find_one({"_id": ObjectId(BO['actuator_id'])}) is None:
            return jsonify({'invalid': BO['actuator_id']}), 400

        name = BO['name']
        tradeMark = BO['tradeMark']
        Model = BO['Model']
        GPIO = BO['GPIO']
        feature_id = BO['feature_id']
        sensor_id = BO['sensor_id']
        actuator_id = BO['actuator_id']

        if Board.find_one({"name": name}) is not None:
            return jsonify({'duplicated': name}), 400
        else:
            Board.insert_one({"name": name, "tradeMark": tradeMark, "Model": Model, "GPIO": GPIO, "feature_id": feature_id,
                      "sensor_id": sensor_id, "actuator_id": actuator_id})

        return jsonify({'name': name}), 200
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ListBoard', methods=['GET'])
@auth.login_required
def ListBoard():
    BO = []
    cursor = Board.find({})

    for document in cursor:
        BO.append({'name': document["name"], 'tradeMark': document["tradeMark"], 'Model': document["Model"], 'GPIO': document["GPIO"],'feature_id': document["feature_id"], 'sensor_id': document["sensor_id"], 'actuator_id':document["actuator_id"]})

    session['BO'] = BO

    return jsonify(BO),200

### Actuator Operations ###

def jsonActuator(AC):
    missing = []
    if len(AC) == 0:
        return jsonify({'missing': 'json null'}), 404
    if not AC:
        return jsonify({'missing': 'json data'}), 400
    if ('name' in AC and AC['name'] == '') or (isinstance(AC['name'], str) != True):
        missing.append('name')
    if 'type' in AC and AC['type'] == '':
        missing.append('type')
    if 'tradeMark' in AC and AC['tradeMark'] == '':
        missing.append('tradeMark')
    if 'Model' in AC and AC['Model'] == '':
        missing.append('Model')
    if 'feature_id' in AC and AC['feature_id'] == '':
        missing.append('feature_id')

    return missing

@application.route('/UpdateActuator', methods=['POST'])
@auth.login_required
def UpdateActuator():
    AC = request.json
    missing = []
    json_update = {}

    if ('name' in AC and AC['name'] == '') or (isinstance(AC['name'], str) != True):
        missing.append('name')

    if missing == []:
        if (AC['feature_id'] != "") and (bson.objectid.ObjectId.is_valid(AC['feature_id']) == False):
            return jsonify({'invalid': 'ObjectID'}), 400
        if (AC['feature_id'] != "") and (Feature.find_one({"_id": ObjectId(AC['feature_id'])})) is None:
            return jsonify({'invalid': AC['feature_id']}), 400

        if 'newname' in AC and AC['newname'] != '':
            json_update['name'] = AC['newname']
        if 'type' in AC and AC['type'] != '':
            json_update['type'] = AC['type']
        if 'tradeMark' in AC and AC['tradeMark'] != '':
            json_update['tradeMark'] = AC['tradeMark']
        if 'Model' in AC and AC['Model'] != '':
            json_update['Model'] = AC['Model']
        if 'value' in AC and AC['value'] != '':
            json_update['value'] = AC['value']
        if 'feature_id' in AC and AC['feature_id'] != '':
            json_update['feature_id'] = AC['feature_id']
        if len(json_update) != 0:
            if Actuator.find_one({"name": AC['newname']}) is not None:
                return jsonify({'duplicated': AC['newname']}), 400
            else:
                document = Actuator.find_one_and_update({"name": AC['name']}, {"$set": json_update}, upsert=False)
        else:
            return jsonify({'missing': 'all components'}), 400
        if document is not None:
            return jsonify({'name': AC['name']}), 200
        else:
            return jsonify({'invalid': AC['name']}), 400
    else:
        return jsonify({'missing': missing}), 400

@application.route('/UpdateValueActuator', methods=['POST'])
@auth.login_required
def UpdateValueActuator():
    missing = []
    AC = request.json

    if ('name' in AC and AC['name'] == '') or (isinstance(AC['name'], str) != True):
        missing.append('name')
    if ('value' in AC and AC['value'] == '') or (isinstance(AC['value'], str) != True):
        missing.append('value')

    if missing == []:
        name = request.json['name']
        Value = request.json['value']

        document = Actuator.find_one_and_update({"name": name}, {"$set": {"value": Value}}, upsert=False)

        if document is not None:
            return jsonify({'name': name}), 200
        else:
            return jsonify({'invalid': name}), 400
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ReadOneActuator',methods=['GET'])
@auth.login_required
def ReadActuator_one():
    AC = []
    name = request.args.get('name', default=1, type=str)
    if name == '':
        return jsonify({'missing': 'name'}), 400
    else:
        doc = Actuator.find_one({"name": name})
        if doc is not None:
            AC.append({'name': doc["name"], 'type': doc["type"], 'tradeMark': doc["tradeMark"], 'Model': doc["Model"],
                       'value': doc["value"], 'feature_id': doc["feature_id"]})
            return jsonify(AC), 200
        else:
            return jsonify({'invalid': name}),400

@application.route('/InsertActuator', methods=['POST'])
@auth.login_required
def InsertActuator():
    AC = request.json
    missing = jsonActuator(AC)

    if missing == []:
        if bson.objectid.ObjectId.is_valid(AC['feature_id']) == False:
            return jsonify({'invalid': 'ObjectID'}), 400
        if Feature.find_one({"_id": ObjectId(AC['feature_id'])}) is None:
            return jsonify({'invalid': AC['feature_id']}), 400

        name = AC['name']
        ttype = AC['type']
        tradeMark = AC['tradeMark']
        Model = AC['Model']
        value = 0
        feature_id = AC['feature_id']

        if Actuator.find_one({"name": name}) is not None:
            return jsonify({'duplicated': name}), 400
        else:
            Actuator.insert_one({"name": name, "type": ttype, "tradeMark": tradeMark,"value":value, "Model": Model, "feature_id": feature_id})

        return jsonify({'name': name}), 200
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ListActuator',methods=['GET'])
@auth.login_required
def ListActuator():
    AC = []
    cursor = Actuator.find({})

    for document in cursor:
        AC.append({'name': document["name"], 'type': document["type"], 'tradeMark': document["tradeMark"], 'Model': document["Model"],'value':document["value"], 'feature_id': document["feature_id"]})

    session['AC'] = AC

    return jsonify(AC),200

### Component Operations ###

def jsonComponent(CO):
    missing = []
    if len(CO) == 0:
        return jsonify({'missing': 'json null'}), 404
    if not CO:
        return jsonify({'missing': 'json data'}), 400
    if ('name' in CO and CO['name'] == '') or (isinstance(CO['name'], str) != True):
        missing.append('name')
    if 'type' in CO and CO['type'] == '':
        missing.append('type')
    if 'tradeMark' in CO and CO['tradeMark'] == '':
        missing.append('tradeMark')
    if 'Model' in CO and CO['Model'] == '':
        missing.append('Model')
    if 'feature_id' in CO and CO['feature_id'] == '':
        missing.append('feature_id')

    return missing

@application.route('/UpdateComponent', methods=['POST'])
@auth.login_required
def UpdateComponent():
    CO = request.json
    missing = []
    json_update = {}

    if ('name' in CO and CO['name'] == '') or (isinstance(CO['name'], str) != True):
        missing.append('name')

    if missing == []:
        if (CO['feature_id'] != "") and (bson.objectid.ObjectId.is_valid(CO['feature_id']) == False):
            return jsonify({'invalid': 'ObjectID'}), 400
        if (CO['feature_id'] != "") and (Feature.find_one({"_id": ObjectId(CO['feature_id'])})) is None:
            return jsonify({'invalid': CO['feature_id']}), 400

        if 'newname' in CO and CO['newname'] != '':
            json_update['name'] = CO['newname']
        if 'type' in CO and CO['type'] != '':
            json_update['type'] = CO['type']
        if 'tradeMark' in CO and CO['tradeMark'] != '':
            json_update['tradeMark'] = CO['tradeMark']
        if 'Model' in CO and CO['Model'] != '':
            json_update['Model'] = CO['Model']
        if 'feature_id' in CO and CO['feature_id'] != '':
            json_update['feature_id'] = CO['feature_id']

        if len(json_update) != 0:
            if Component.find_one({"name": CO['newname']}) is not None:
                return jsonify({'duplicated': CO['newname']}), 400
            else:
                document = Component.find_one_and_update({"name": CO['name']}, {"$set": json_update},upsert=False)
        else:
            return jsonify({'missing': 'all components'}), 400
        if document is not None:
            return jsonify({'name': CO['name']}), 200
        else:
            return jsonify({'invalid': CO['name']}), 400
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ReadOneComponent', methods=['GET'])
@auth.login_required
def ReadComponent_one():
    CO = []
    name = request.args.get('name', default=1, type=str)
    if name == '':
        return jsonify({'missing': 'name'}), 400
    else:
        doc = Component.find_one({"name": name})
        if doc is not None:
            CO.append({'name': doc["name"], 'type': doc["type"], 'tradeMark': doc["tradeMark"], 'Model': doc["Model"],
                       'feature_id': doc["feature_id"]})
            return jsonify(CO), 200
        else:
            return jsonify({'invalid': name}),400

@application.route('/InsertComponent', methods=['POST'])
@auth.login_required
def InsertComponent():
    CO = request.json
    missing = jsonComponent(CO)

    if missing == []:
        if bson.objectid.ObjectId.is_valid(CO['feature_id']) == False:
            return jsonify({'invalid': 'ObjectID'}), 400
        if Feature.find_one({"_id": ObjectId(CO['feature_id'])}) is None:
            return jsonify({'invalid': CO['feature_id']}), 400

        name = CO['name']
        ttype = CO['type']
        tradeMark = CO['tradeMark']
        Model = CO['Model']
        feature_id = CO['feature_id']

        if Component.find_one({"name": name}) is not None:
            return jsonify({'duplicated': name}), 400
        else:
            Component.insert_one({"name": name, "type": ttype, "tradeMark": tradeMark, "Model": Model, "feature_id": feature_id})

        return jsonify({'name': name}), 200
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ListComponent', methods=['GET'])
@auth.login_required
def ListComponent():
    CO = []
    cursor = Component.find({})

    for document in cursor:
        CO.append({'name': document["name"], 'type': document["type"], 'tradeMark': document["tradeMark"], 'Model':document["Model"],'feature_id': document["feature_id"]})

    session['CO'] = CO

    return jsonify(CO),200

### Experiment Operations ###

def jsonExperiment(EX):
    missing = []

    if len(EX) == 0:
        return jsonify({'missing': 'json null'}), 404
    if not EX:
        return jsonify({'missing': 'json data'}), 400
    if ('name' in EX and EX['name'] == '') or (isinstance(EX['name'], str) != True):
        missing.append('name')
    if 'priority' in EX and EX['priority'] == '':
        missing.append('priority')
    if 'board_id' in EX and EX['board_id'] == '':
        missing.append('board_id')
    if 'component_id' in EX and EX['component_id'] == '':
        missing.append('component_id')
    if 'feature_id' in EX and EX['feature_id'] == '':
        missing.append('feature_id')

    return missing

@application.route('/UpdateExperiment', methods=['POST'])
@auth.login_required
def UpdateExperiment():
    EX = request.json
    missing = []
    json_update = {}

    if ('name' in EX and EX['name'] == '') or (isinstance(EX['name'], str) != True):
        missing.append('name')

    if missing == []:
        if (EX['board_id'] != "") and (bson.objectid.ObjectId.is_valid(EX['board_id']) == False) or \
                (EX['component_id'] != "") and (bson.objectid.ObjectId.is_valid(EX['component_id']) == False) or \
                (EX['feature_id'] != "") and (bson.objectid.ObjectId.is_valid(EX['feature_id']) == False):
            return jsonify({'invalid': 'ObjectID'}), 400
        if (EX['board_id'] != "") and (Board.find_one({"_id": ObjectId(EX['board_id'])})) is None:
            return jsonify({'invalid': EX['board_id']}), 400
        if (EX['component_id'] != "") and (Component.find_one({"_id": ObjectId(EX['component_id'])})) is None:
            return jsonify({'invalid': EX['component_id']}), 400
        if (EX['feature_id'] != "") and (Feature.find_one({"_id": ObjectId(EX['feature_id'])})) is None:
            return jsonify({'invalid': EX['feature_id']}), 400

        if 'newname' in EX and EX['newname'] != '':
            json_update['name'] = EX['newname']
        if 'priority' in EX and EX['priority'] != '':
            json_update['priority'] = EX['priority']
        if 'board_id' in EX and EX['board_id'] != '':
            json_update['board_id'] = EX['board_id']
        if 'component_id' in EX and EX['component_id'] != '':
            json_update['component_id'] = EX['component_id']
        if 'feature_id' in EX and EX['feature_id'] != '':
            json_update['feature_id'] = EX['feature_id']
        if len(json_update) != 0:
            if Experiment.find_one({"name": EX['newname']}) is not None:
                return jsonify({'duplicated': EX['newname']}), 400
            else:
                document = Experiment.find_one_and_update({"name": EX['name']}, {"$set": json_update}, upsert=False)
        else:
            return jsonify({'missing': 'all components'}), 400
        if document is not None:
            return jsonify({'name': EX['name']}), 200
        else:
            return jsonify({'invalid': EX['name']}), 400
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ReadOneExperiment', methods=['GET'])
@auth.login_required
def ReadExperiment_one():
    EX = []
    name = request.args.get('name', default=1, type=str)
    if name == '':
        return jsonify({'missing': 'name'}), 400
    else:
        doc = Experiment.find_one({"name": name})
        if doc is not None:
            EX.append({'name': doc["name"], 'priority': doc["priority"], 'board_id': doc["board_id"],
                       'component_id': doc["component_id"], 'feature_id': doc["feature_id"]})
            return jsonify(EX), 200
        else:
            return jsonify({'invalid': name}),400

@application.route('/InsertExperiment', methods=['POST'])
@auth.login_required
def InsertExperiment():
    EX = request.json
    missing = jsonExperiment(EX)

    if missing == []:

        if (bson.objectid.ObjectId.is_valid(EX['board_id']) == False)  or (bson.objectid.ObjectId.is_valid(EX['component_id']) == False) or (bson.objectid.ObjectId.is_valid(EX['feature_id']) == False):
            return jsonify({'invalid': 'ObjectID'}), 400
        if Board.find_one({"_id": ObjectId(EX['board_id'])}) is None:
            return jsonify({'invalid': EX['board_id']}), 400
        if Component.find_one({"_id": ObjectId(EX['component_id'])}) is None:
            return jsonify({'invalid': EX['component_id']}), 400
        if Feature.find_one({"_id": ObjectId(EX['feature_id'])}) is None:
            return jsonify({'invalid': EX['feature_id']}), 400

        name = EX['name']
        priority = EX['priority']
        board_id = EX['board_id']
        component_id = EX['component_id']
        feature_id = EX['feature_id']

        if Experiment.find_one({"name": name}) is not None:
            return jsonify({'duplicated': name}), 400
        else:
            Experiment.insert_one({"name": name, "priority": priority, "board_id": board_id, "component_id": component_id,
                           "feature_id": feature_id})

        return jsonify({'name': name}), 200
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ListExperiment', methods=['GET'])
@auth.login_required
def ListExperiment():
    EX = []
    cursor = Experiment.find({})

    for document in cursor:
        EX.append({'name': document["name"], 'priority': document["priority"], 'board_id': document["board_id"],'component_id': document["component_id"],'feature_id': document["feature_id"]})

    session['EX'] = EX

    return jsonify(EX),200

### Feature Operations ###

def jsonFeature(FE):
    missing = []

    if len(FE) == 0:
        return jsonify({'missing': 'json null'}), 404
    if not FE:
        return jsonify({'missing': 'json data'}), 400
    if ('name' in FE and FE['name'] == '') or (isinstance(FE['name'], str) != True):
        missing.append('name')
    if 'type' in FE and FE['type'] == '':
        missing.append('type')
    if 'maxValue' in FE and FE['maxValue'] == '':
        missing.append('maxValue')
    if 'minValue' in FE and FE['minValue'] == '':
        missing.append('minValue')

    return missing

@application.route('/UpdateFeature', methods=['POST'])
@auth.login_required
def UpdateFeature():
    FE = request.json
    missing = []
    json_update = {}
    if ('name' in FE and FE['name'] == '') or (isinstance(FE['name'], str) != True):
        missing.append('name')

    if missing == []:

        if 'newname' in FE and FE['newname'] != '':
            json_update['name'] = FE['newname']
        if 'type' in FE and FE['type'] != '':
            json_update['type'] = FE['type']
        if 'maxValue' in FE and FE['maxValue'] != '':
            json_update['maxValue'] = FE['maxValue']
        if 'minValue' in FE and FE['minValue'] != '':
            json_update['minValue'] = FE['minValue']

        if len(json_update) != 0:
            if Feature.find_one({"name": FE['newname']}) is not None:
                return jsonify({'duplicated': FE['newname']}), 400
            else:
                document = Feature.find_one_and_update({"name": FE['name']}, {"$set": json_update}, upsert=False)
        else:
            return jsonify({'missing': 'all components'}), 400
        if document is not None:
            return jsonify({'name': FE['name']}), 200
        else:
            return jsonify({'invalid': FE['name']}), 400
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ReadOneFeature', methods=['GET'])
@auth.login_required
def ReadFeature_one():
    FE = []
    name = request.args.get('name', default=1, type=str)
    if name == '':
        return jsonify({'missing': 'name'}), 400
    else:
        doc = Feature.find_one({"name": name})
        if doc is not None:
            FE.append({'name': doc["name"], 'type': doc["type"], 'maxValue': doc["maxValue"], 'minValue': doc["minValue"]})
            return jsonify(FE), 200
        else:
            return jsonify({'invalid': name}),400

@application.route('/InsertFeature', methods=['POST'])
@auth.login_required
def InsertFeature():
    missing = jsonFeature(request.json)

    if missing == []:
        name = request.json['name']
        ttype = request.json['type']
        maxValue = request.json['maxValue']
        minValue = request.json['minValue']

        if Feature.find_one({"name": name}) is not None:
            return jsonify({'duplicated': name}), 400
        else:
            Feature.insert_one({"name": name, "type": ttype, "maxValue": maxValue, "minValue": minValue})

        return jsonify({'name': name}), 200
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ListFeature', methods=['GET'])
@auth.login_required
def ListFeature():
    FE = []
    cursor = Feature.find({})

    for document in cursor:
        FE.append({'name': document["name"], 'type': document["type"], 'maxValue': document["maxValue"],
                       'minValue': document["minValue"]})

    session['FE'] = FE

    return jsonify(FE),200

### People Operations ###

def jsonPeople(PE):
    missing = []

    if len(PE) == 0:
        return jsonify({'missing': 'json null'}), 404
    if not PE:
        return jsonify({'missing': 'json data'}), 400
    if ('name' in PE and PE['name'] == '') or (isinstance(PE['name'], str) != True):
        missing.append('name')
    if 'surname' in PE and PE['surname'] == '':
        missing.append('surname')
    if 'function' in PE and PE['function'] == '':
        missing.append('function')
    if 'birth' in PE and PE['birth'] == '':
        missing.append('birth')
    if 'register' in PE and PE['register'] == '':
        missing.append('register')
    if 'email' in PE and PE['email'] == '':
        missing.append('email')
    if 'login' in PE and PE['login'] == '':
        missing.append('login')
    if 'register' in PE and PE['register'] == '':
        missing.append('register')
    if 'email' in PE and PE['email'] == '':
        missing.append('email')
    if 'login' in PE and PE['login'] == '':
        missing.append('login')
    if 'password' in PE and PE['password'] == '':
        missing.append('password')
    if 'CPF' in PE and PE['CPF'] == '':
        missing.append('CPF')
    if 'RG' in PE and PE['RG'] == '':
        missing.append('RG')
    if 'institute_id' in PE and PE['institute_id'] == '':
        missing.append('institute_id')

    return missing

@application.route('/UpdatePeople', methods=['POST'])
@auth.login_required
def UpdatePeople():
    PE = request.json
    missing = []
    json_update = {}
    if ('name' in PE and PE['name'] == '') or (isinstance(PE['name'], str) != True):
        missing.append('name')

    if missing == []:
        if (PE['institute_id'] != "") and (bson.objectid.ObjectId.is_valid(PE['institute_id']) == False):
            return jsonify({'invalid': 'ObjectID'}), 400
        if (PE['institute_id'] != "") and (Institute.find_one({"_id": ObjectId(PE['institute_id'])})) is None:
            return jsonify({'invalid': PE['institute_id']}), 400

        if 'newname' in PE and PE['newname'] != '':
            json_update['name'] = PE['newname']
        if 'surname' in PE and PE['surname'] != '':
            json_update['surname'] = PE['surname']
        if 'function' in PE and PE['function'] != '':
            json_update['function'] = PE['function']
        if 'birth' in PE and PE['birth'] != '':
            json_update['birth'] = PE['birth']
        if 'register' in PE and PE['register'] != '':
            json_update['register'] = PE['register']
        if 'email' in PE and PE['email'] != '':
            json_update['email'] = PE['email']
        if 'login' in PE and PE['login'] != '':
            json_update['login'] = PE['login']
        if 'password' in PE and PE['password'] != '':
            json_update['password'] = PE['password']
        if 'CPF' in PE and PE['CPF'] != '':
            json_update['CPF'] = PE['CPF']
        if 'RG' in PE and PE['RG'] != '':
            json_update['RG'] = PE['RG']
        if 'institute_id' in PE and PE['institute_id'] != '':
            json_update['institute_id'] = PE['institute_id']

        if len(json_update) != 0:
            if People.find_one({"CPF": PE['CPF']}) is not None:
                return jsonify({'duplicated': PE['CPF']}), 400
            if People.find_one({"RG": PE['RG']}) is not None:
                return jsonify({'duplicated': PE['RG']}), 400
            else:
                document = People.find_one_and_update({"name": PE['name']}, {"$set": json_update}, upsert=False)
        else:
            return jsonify({'missing': 'all components'}), 400
        if document is not None:
            return jsonify({'name': PE['name']}), 200
        else:
            return jsonify({'invalid': PE['name']}), 400
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ReadOnePeople', methods=['GET'])
@auth.login_required
def ReadPeople_one():
    PE = []
    name = request.args.get('name', default=1, type=str)
    if name == '':
        return jsonify({'missing': 'name'}), 400
    else:
        doc = People.find_one({"name": name})
        if doc is not None:
            PE.append(
                {'name': doc["name"], 'surname': doc["surname"], 'function': doc["function"], 'birth': doc["birth"],
                 'register': doc["register"], 'email': doc["email"], 'login': doc["login"], 'password': doc["password"],
                 'CPF': doc["CPF"], 'RG': doc["RG"], 'institute_id': doc["institute_id"]})
            return jsonify(PE), 200
        else:
            return jsonify({'invalid': name}), 400

@application.route('/InsPeople', methods=['POST'])
@auth.login_required
def InsPeople():
    PE = request.json
    print(PE)
    missing = jsonPeople(PE)

    if missing == []:
        print("Missing!")
        if bson.objectid.ObjectId.is_valid(PE['institute_id']) == False:
            return jsonify({'invalid': 'ObjectID'}), 400
        if Institute.find_one({"_id": ObjectId(PE['institute_id'])}) is None:
            return jsonify({'invalid': PE['institute_id']}), 400

        name = PE['name']
        surname = PE['surname']
        ffunction = PE['function']
        birth = PE['birth']
        register = PE['register']
        email = PE['email']
        login = PE['login']
        password = PE['password']
        CPF = PE['CPF']
        RG = PE['RG']
        institute_id = PE['institute_id']

        if People.find_one({"CPF": CPF}) is not None:
            print("Tem CPF");
            return jsonify({'duplicated': CPF}), 400
        if People.find_one({"RG": RG}) is not None:
            print("Tem RG");
            return jsonify({'duplicated': RG}), 400
        else:
            print("Inseri");
            People.insert_one({"name": name, "surname": surname, "function": ffunction, "birth": birth, "register": register,
                           "email": email, "login": login, "password": password, "CPF": CPF, "RG": RG,
                           "institute_id": institute_id})

        return jsonify({'name': name}), 200
    else:
        print("Componente");
        return jsonify({'missing': missing}), 400

@application.route('/ListPeople', methods=['GET'])
@auth.login_required
def ListPeople():
    PE = []
    cursor = People.find({})

    for document in cursor:
        PE.append({'name': document["name"], 'surname': document["surname"], 'function': document["function"],
                   'birth': document["birth"],'register': document["register"],'email': document["email"],'login': document["login"],
                   'password': document["password"],'CPF': document["CPF"],'RG': document["RG"],'institute_id': document["institute_id"]})

    session['PE'] = PE

    return jsonify(PE),200

### Request Operations ###

def jsonRequest(RE):
    missing = []

    if len(RE) == 0:
        return jsonify({'missing': 'json null'}), 404
    if not RE:
        return jsonify({'missing': 'json data'}), 400
    if ('dateTime' in RE and RE['dateTime'] == '') or (isinstance(RE['dateTime'], str) != True):
        missing.append('dateTime')
    if 'duration' in RE and RE['duration'] == '':
        missing.append('duration')
    if 'People_id' in RE and RE['People_id'] == '':
        missing.append('People_id')
    if 'Experiment_id' in RE and RE['Experiment_id'] == '':
        missing.append('Experiment_id')
    return missing

@application.route('/UpdateRequest', methods=['POST'])
@auth.login_required
def UpdateRequest():
    RE = request.json
    missing = []
    json_update = {}

    if ('dateTime' in RE and RE['dateTime'] == '') or (isinstance(RE['dateTime'], str) != True):
        missing.append('dateTime')

    if missing == []:
        if (RE['People_id'] != "") and (bson.objectid.ObjectId.is_valid(RE['People_id']) == False) or (RE['Experiment_id'] != "") and (bson.objectid.ObjectId.is_valid(RE['Experiment_id']) == False):
            return jsonify({'invalid': 'ObjectID'}), 400
        if (RE['People_id'] != "") and (People.find_one({"_id": ObjectId(RE['People_id'])})) is None:
            return jsonify({'invalid': RE['People_id']}), 400
        if (RE['Experiment_id'] != "") and (Experiment.find_one({"_id": ObjectId(RE['Experiment_id'])})) is None:
            return jsonify({'invalid': RE['Experiment_id']}), 400
        if 'newdateTime' in RE and RE['newdateTime'] != '':
            json_update['dateTime'] = RE['newdateTime']
        if 'duration' in RE and RE['duration'] != '':
            json_update['duration'] = RE['duration']
        if 'People_id' in RE and RE['People_id'] != '':
            json_update['People_id'] = RE['People_id']
        if 'Experiment_id' in RE and RE['Experiment_id'] != '':
            json_update['Experiment_id'] = RE['Experiment_id']

        if len(json_update) != 0:
            if Request.find_one({"dateTime": RE['newdateTime']}) is not None:
                return jsonify({'duplicated': RE['newdateTime']}), 400
            else:
                document = Request.find_one_and_update({"dateTime": RE['dateTime']}, {"$set": json_update}, upsert=False)
        else:
            return jsonify({'missing': 'all components'}), 400
        if document is not None:
            return jsonify({'dateTime': RE['dateTime']}), 200
        else:
            return jsonify({'invalid': RE['dateTime']}), 400
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ReadOneRequest')
@auth.login_required
def ReadRequest_one():
    RE = []
    dateTime = request.args.get('dateTime', default=1, type=str)
    print(dateTime)
    if dateTime == '':
        print('IF NULL')
        return jsonify({'missing': 'dateTime'}), 400
    else:
        print('else')
        doc = Request.find_one({"dateTime": dateTime})
        if doc is not None:
            RE.append({'dateTime': doc["dateTime"], 'duration': doc["duration"], 'People_id': doc["People_id"],
                       'Experiment_id': doc["Experiment_id"]})
            return jsonify(RE), 200
        else:
            return jsonify({'invalid': dateTime}),400

@application.route('/InsertReq', methods=['POST'])
@auth.login_required
def InsertReq():
    RE = request.json
    missing = jsonRequest(RE)

    if missing == []:
        if (bson.objectid.ObjectId.is_valid(RE['People_id']) == False)  or (bson.objectid.ObjectId.is_valid(RE['Experiment_id']) == False):
            return jsonify({'invalid': 'ObjectID'}), 400
        if People.find_one({"_id": ObjectId(RE['People_id'])}) is None:
            return jsonify({'invalid': RE['People_id']}), 400
        if Experiment.find_one({"_id": ObjectId(RE['Experiment_id'])}) is None:
            return jsonify({'invalid': RE['Experiment_id']}), 400

        dateTime = RE['dateTime']
        duration = RE['duration']
        People_id = RE['People_id']
        Experiment_id = RE['Experiment_id']

        if Request.find_one({"dateTime": dateTime}) is not None:
            return jsonify({'duplicated': dateTime}), 400
        else:
            Request.insert_one({"dateTime": dateTime, "duration": duration, "People_id": People_id, "Experiment_id": Experiment_id})

        return jsonify({'dateTime': dateTime}), 200
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ListRequest', methods=['GET'])
@auth.login_required
def ListRequest():
    RE = []
    cursor = Request.find({})

    for document in cursor:
        RE.append({'dateTime': document["dateTime"], 'duration': document["duration"], 'People_id': document["People_id"],
                   'Experiment_id': document["Experiment_id"]})

    session['RE'] = RE

    return jsonify(RE),200

### Sensor Operations ###

def jsonSensor(SE):
    missing = []

    if len(SE) == 0:
        return jsonify({'missing': 'json null'}), 404
    if not SE:
        return jsonify({'missing': 'json data'}), 400
    if ('name' in SE and SE['name'] == '') or (isinstance(SE['name'], str) != True):
        missing.append('name')
    if 'type' in SE and SE['type'] == '':
        missing.append('type')
    if 'TradeMark' in SE and SE['TradeMark'] == '':
        missing.append('TradeMark')
    if 'Model' in SE and SE['Model'] == '':
        missing.append('Model')
    if 'feature_id' in SE and SE['feature_id'] == '':
        missing.append('feature_id')
    return missing

@application.route('/UpdateSensor', methods=['POST'])
@auth.login_required
def UpdateSensor():
    SE = request.json
    missing = []
    json_update = {}

    if ('name' in SE and SE['name'] == '') or (isinstance(SE['name'], str) != True):
        missing.append('name')

    if missing == []:
        if (SE['feature_id'] != "") and (bson.objectid.ObjectId.is_valid(SE['feature_id']) == False):
            return jsonify({'invalid': 'ObjectID'}), 400
        if (SE['feature_id'] != "") and (Feature.find_one({"_id": ObjectId(SE['feature_id'])})) is None:
            return jsonify({'invalid': SE['feature_id']}), 400

        if 'newname' in SE and SE['newname'] != '':
            json_update['name'] = SE['newname']
        if 'type' in SE and SE['type'] != '':
            json_update['type'] = SE['type']
        if 'tradeMark' in SE and SE['tradeMark'] != '':
            json_update['tradeMark'] = SE['tradeMark']
        if 'Model' in SE and SE['Model'] != '':
            json_update['Model'] = SE['Model']
        if 'value' in SE and SE['value'] != '':
            json_update['value'] = SE['value']
        if 'feature_id' in SE and SE['feature_id'] != '':
            json_update['feature_id'] = SE['feature_id']
        if len(json_update) != 0:
            if Sensor.find_one({"name": SE['newname']}) is not None:
                return jsonify({'duplicated': SE['newname']}), 400
            else:
                document = Sensor.find_one_and_update({"name": SE['name']}, {"$set": json_update}, upsert=False)
        else:
            return jsonify({'missing': 'all components'}), 400
        if document is not None:
            return jsonify({'name': SE['name']}), 200
        else:
            return jsonify({'invalid': SE['name']}), 400
    else:
        return jsonify({'missing': missing}), 400

@application.route('/UpdateValueSensor', methods=['POST'])
@auth.login_required
def UpdateValueSensor():
    missing = []
    SE = request.json

    if ('name' in SE and SE['name'] == '') or (isinstance(SE['name'], str) != True):
        missing.append('name')
    if ('value' in SE and SE['value'] == '') or (isinstance(SE['value'], str) != True):
        missing.append('value')

    if missing == []:
        name = request.json['name']
        Value = request.json['value']

        document = Sensor.find_one_and_update({"name": name}, {"$set": {"value": Value}}, upsert=False)

        if document is not None:
            return jsonify({'name': name}), 200
        else:
            return jsonify({'invalid': name}), 400
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ReadOneSensor', methods=['GET'])
@auth.login_required
def ReadSensor_one():
    SE = []
    name = request.args.get('name', default=1, type=str)
    if name == '':
        return jsonify({'missing': 'name'}), 400
    else:
        doc = Sensor.find_one({"name": name})
        if doc is not None:
            SE.append({'name': doc["name"], 'type': doc["type"], 'TradeMark': doc["TradeMark"], 'Model': doc["Model"],
                       'value': doc["value"], 'feature_id': doc["feature_id"]})
            return jsonify(SE), 200
        else:
            return jsonify({'invalid': name}), 400

@application.route('/InsertSensor', methods=['POST'])
@auth.login_required
def InsertSensor():
    SE = request.json
    missing = jsonSensor(SE)

    if missing == []:
        if bson.objectid.ObjectId.is_valid(SE['feature_id']) == False:
            return jsonify({'invalid': 'ObjectID'}), 400
        if Feature.find_one({"_id": ObjectId(SE['feature_id'])}) is None:
            return jsonify({'invalid': SE['feature_id']}), 400

        name = SE['name']
        ttype = SE['type']
        TradeMark = SE['TradeMark']
        Model = SE['Model']
        value = 0
        feature_id = SE['feature_id']

        if Sensor.find_one({"name": name}) is not None:
            return jsonify({'duplicated': name}), 400
        else:
            Sensor.insert_one({"name": name, "type": ttype, "TradeMark": TradeMark, "Model": Model, "value": value,
                       "feature_id": feature_id})

        return jsonify({'name': name}), 200
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ListSensor', methods=['GET'])
@auth.login_required
def ListSensor():
    SE = []
    cursor = Sensor.find({})

    for document in cursor:
        SE.append(
            {'name': document["name"], 'type': document["type"], 'TradeMark': document["TradeMark"],
             'Model': document["Model"],'value': document["value"],'feature_id': document["feature_id"]})

    session['SE'] = SE

    return jsonify(SE),200

### Quiz Operations ###

def jsonQuiz(QI):
    missing = []

    if len(QI) == 0:
        return jsonify({'missing': 'json null'}), 404
    if not QI:
        return jsonify({'missing': 'json data'}), 400
    if ('name' in QI and QI['name'] == '') or (isinstance(QI['name'],str) != True) :
        missing.append('name')
    if 'question' in QI and QI['question'] == '':
        missing.append('question')
    if 'response' in QI and QI['response'] == '':
        missing.append('response')
    if 'response_option' in QI and QI['response_option'] == '':
        missing.append('response_option')
    if 'experiment_id' in QI and QI['experiment_id'] == '':
        missing.append('experiment_id')
    return(missing)

@application.route('/UpdateQuiz', methods=['POST'])
@auth.login_required
def UpdateQuiz():
    QI = request.json
    missing = []
    json_update = {}

    if ('name' in QI and QI['name'] == '') or (isinstance(QI['name'],str) != True) :
        missing.append('name')

    if missing == []:
        if (QI['experiment_id'] != "") and (bson.objectid.ObjectId.is_valid(QI['experiment_id']) == False):
            return jsonify({'invalid': 'ObjectID'}), 400
        if (QI['experiment_id'] != "") and (Experiment.find_one({"_id": ObjectId(QI['experiment_id'])})) is None:
            return jsonify({'invalid': QI['experiment_id']}), 400

        if 'newname' in QI and QI['newname'] != '':
            json_update['name']=QI['newname']
        if 'question' in QI and QI['question'] != '':
            json_update['question']=QI['question']
        if 'response' in QI and QI['response'] != '':
            json_update['response']=QI['response']
        if 'response_option' in QI and QI['response_option'] != '':
            json_update['response_option']=QI['response_option']
        if 'experiment_id' in QI and QI['experiment_id'] != '':
            json_update['experiment_id']=QI['experiment_id']
        if len(json_update) != 0:
            if Quiz.find_one({"name": QI['newname']}) is not None:
                return jsonify({'duplicated': QI['newname']}), 400
            else:
                document = Quiz.find_one_and_update({"name": QI['name']}, {"$set": json_update}, upsert=False)
        else:
            return jsonify({'missing': 'all components'}), 400
        if document is not None:
            return jsonify({'name': QI['name']}), 200
        else:
            return jsonify({'invalid': QI['name']}), 400
    else:
        return jsonify({'missing': missing}), 400

@application.route('/ReadOneQuiz', methods=['GET'])
@auth.login_required
def ReadQuiz_one():
    QI = []
    name = request.args.get('name', default=1, type = str)
    if name == '':
        return jsonify({'missing':'name'}), 400
    else:
        doc = Quiz.find_one({"name": name})
        if doc is not None:
            QI.append({'name': doc["name"], 'question': doc["question"], 'response': doc["response"], 'response_option': doc["response_option"],'experiment_id': doc["experiment_id"]})
            return jsonify(QI), 200
        else:
            return jsonify({'invalid': name}),400

@application.route('/InsertQuiz', methods=['POST'])
@auth.login_required
def InsertQuiz():
    QI = request.json
    missing = jsonQuiz(QI)

    if missing == []:

        if bson.objectid.ObjectId.is_valid(QI['experiment_id']) == False:
            return jsonify({'invalid': 'ObjectID'}), 400
        if Experiment.find_one({"_id": ObjectId(QI['experiment_id'])}) is None:
            return jsonify({'invalid': QI['experiment_id']}), 400

        name = QI['name']
        question = QI['question']
        response = QI['response']
        response_option = QI['response_option']
        experiment_id = QI['experiment_id']

        if Quiz.find_one({"name": name}) is not None:
            return jsonify({'duplicated': name}), 400
        else:
            Quiz.insert_one({"name": name, "question": question, "response": response, "response_option": response_option, "experiment_id": experiment_id})
        return jsonify({'name': name}),200

    else:
        return jsonify({'missing': missing}),400

@application.route('/ListQuiz', methods=['GET'])
@auth.login_required
def ListQuiz():
    QI = []
    cursor = Quiz.find({})

    for document in cursor:
        QI.append({'name': document["name"], 'question': document["question"], 'response': document["response"],'response_option': document["response_option"], 'experiment_id': document["experiment_id"]})
    session['QI'] = QI

    return jsonify(QI),200

def jsonEventSensor(EV):
    missing = []

    if len(EV) == 0:
        return jsonify({'missing': 'json null'}), 404
    if not EV:
        return jsonify({'missing': 'json data'}), 400
    if ('sensor_id' in EV and EV['sensor_id'] == '') or (isinstance(EV['sensor_id'], str) != True):
        missing.append('sensor_id')
    if 'value' in EV and EV['value'] == '':
        missing.append('value')
    if 'datetime' in EV and EV['datetime'] == '':
        missing.append('datetime')
    if 'request_id' in EV and EV['request_id'] == '':
        missing.append('request_id')
    if 'experiment_id' in EV and EV['experiment_id'] == '':
        missing.append('experiment_id')
    if 'people_id' in EV and EV['people_id'] == '':
        missing.append('people_id')
    return missing

@application.route('/EventSensor', methods=['POST'])
def EventSensor():
    EV = request.json
    missing = jsonEventSensor(EV)

    if missing == []:

        if (bson.objectid.ObjectId.is_valid(EV['sensor_id']) == False)  or\
            (bson.objectid.ObjectId.is_valid(EV['request_id']) == False) or\
            (bson.objectid.ObjectId.is_valid(EV['experiment_id']) == False) or\
            (bson.objectid.ObjectId.is_valid(EV['people_id']) == False):
            return jsonify({'invalid': 'ObjectID'}), 400

        if Sensor.find_one({"_id": ObjectId(EV['sensor_id'])}) is None:
            return jsonify({'invalid': EV['sensor_id']}), 400
        if Request.find_one({"_id": ObjectId(EV['request_id'])}) is None:
            return jsonify({'invalid': EV['request_id']}), 400
        if Experiment.find_one({"_id": ObjectId(EV['experiment_id'])}) is None:
            return jsonify({'invalid': EV['experiment_id']}), 400
        if People.find_one({"_id": ObjectId(EV['people_id'])}) is None:
            return jsonify({'invalid': EV['people_id']}), 400

        sensor_id = EV['sensor_id']
        value = EV['value']
        datetime = EV['datetime']
        request_id = EV['request_id']
        experiment_id = EV['experiment_id']
        people_id = EV['people_id']

        Event.insert_one({"sensor_id": sensor_id, "value": value, "datetime": datetime, "request_id":request_id,"experiment_id":experiment_id,"people_id":people_id})

        return jsonify({'sensor_id': sensor_id}), 200
    else:
        return jsonify({'missing': missing}), 400

def jsonEventActuator(EV):
    missing = []

    if len(EV) == 0:
        return jsonify({'missing': 'json null'}), 404
    if not EV:
        return jsonify({'missing': 'json data'}), 400
    if ('actuator_id' in EV and EV['actuator_id'] == '') or (isinstance(EV['actuator_id'], str) != True):
        missing.append('actuator_id')
    if 'value' in EV and EV['value'] == '':
        missing.append('value')
    if 'datetime' in EV and EV['datetime'] == '':
        missing.append('datetime')
    if 'request_id' in EV and EV['request_id'] == '':
        missing.append('request_id')
    if 'experiment_id' in EV and EV['experiment_id'] == '':
        missing.append('experiment_id')
    if 'people_id' in EV and EV['people_id'] == '':
        missing.append('people_id')
    return missing

@application.route('/EventActuator', methods=['POST'])
def EventActuator():
    EV = request.json
    missing = jsonEventActuator(EV)

    if missing == []:

        if (bson.objectid.ObjectId.is_valid(EV['actuator_id']) == False) or \
                (bson.objectid.ObjectId.is_valid(EV['request_id']) == False) or \
                (bson.objectid.ObjectId.is_valid(EV['experiment_id']) == False) or \
                (bson.objectid.ObjectId.is_valid(EV['people_id']) == False):
            return jsonify({'invalid': 'ObjectID'}), 400

        if Actuator.find_one({"_id": ObjectId(EV['actuator_id'])}) is None:
            return jsonify({'invalid': EV['actuator_id']}), 400
        if Request.find_one({"_id": ObjectId(EV['request_id'])}) is None:
            return jsonify({'invalid': EV['request_id']}), 400
        if Experiment.find_one({"_id": ObjectId(EV['experiment_id'])}) is None:
            return jsonify({'invalid': EV['experiment_id']}), 400
        if People.find_one({"_id": ObjectId(EV['people_id'])}) is None:
            return jsonify({'invalid': EV['people_id']}), 400

        actuator_id = EV['actuator_id']
        value = EV['value']
        datetime = EV['datetime']
        request_id = EV['request_id']
        experiment_id = EV['experiment_id']
        people_id = EV['people_id']

        Event.insert_one({"actuator_id": actuator_id, "value": value, "datetime": datetime, "request_id":request_id,"experiment_id":experiment_id,"people_id":people_id})

        return jsonify({'actuator_id': actuator_id}), 200
    else:
        return jsonify({'missing': missing}), 400

if __name__ == "__main__":
    application.run(host="0.0.0.0", port='8080')
